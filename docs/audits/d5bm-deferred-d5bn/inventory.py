# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only D5BN inventory. Run from the repository root with Python -I -S -B.

Only the standard library and read-only Git commands are used. Paths in the
output are repository-relative. Keep --full output local. No fixture imports.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import zipfile


ROOT = Path.cwd().resolve()
LOCAL = Path(".local-work/d5bm")
ATTEMPTS = LOCAL / "admission-attempts"
R3 = LOCAL / "correction-delivery-r3/manifest.json"
REVIEW = LOCAL / "correction-admission-review-r3.md"
PROTECTION = LOCAL / "postflight.json"
PUMP_PERMIT = LOCAL / "r3-review-pump-launcher-keys.json"
TAGS_PERMIT = LOCAL / "r3-review-tags-launcher-keys.json"
REPO_ENV = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
ATTEMPT_CASES = {"r3-pump-normal03": "normal", "r3-pump-pending01": "pending",
                 "r3-pump-missing01": "missing"}
RESULTS = {"normal": "RECEIPTED COMPONENT", "pending": "REFUSED", "missing": "RECEIPTED CONTRAST"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def git(*args):
    return subprocess.check_output(["git", *args], env=REPO_ENV, text=True).strip("\n")


def pins(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
         "Expected a regular, non-reparse file")
    with path.open("rb") as stream:
        return {"bytes": info.st_size, "sha256": hashlib.file_digest(stream, "sha256").hexdigest()}


def sha(path):
    return pins(path)["sha256"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def full_members(root):
    for base, dirs, names in os.walk(root):
        for name in dirs:
            info = (Path(base) / name).lstat()
            need(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                 "Refusing to traverse a reparse directory")
        for name in names:
            path = Path(base) / name
            yield path.as_posix(), pins(path)


def r3_attempt(folder, case, permit):
    admission = load(folder / "admission.json")
    post = load(folder / "postflight.json")
    owner = load(folder / "owner.json")
    need(admission["attempt"] == folder.name and admission["case"] == case, "Wrong attempt identity")
    need(admission["review"] == sha(PUMP_PERMIT) and admission["sources"] == permit["sources"]
         and admission["runtime"] == permit["runtime"] and admission["protected"] == sha(PROTECTION)
         and all(admission[key] == permit[key] for key in ("head", "tree", "index", "reviewer"))
         and admission["interpreterHash"] == permit["interpreter"], "Admission identity mismatch")
    argv = admission["argv"]
    need(argv[:4] == ["-I", "-S", "-B", "-X"] and argv[4] == "faulthandler"
         and Path(argv[5]).name == "d5bm_pump_probe.py"
         and Path(argv[5]).relative_to(ROOT).as_posix() == (folder / "source/research/"
             "resource-retained-population/d5bm_pump_probe.py").as_posix()
         and argv[6:] == ["--exe", load(PROTECTION)["protected"][0]["path"].replace("\\", "/"),
                         "--case", case], "Invocation mismatch")
    actual = {name: row["sha256"] for name, row in full_members(folder / "source")}
    expected = {(folder / "source" / name).as_posix(): digest for name, digest in permit["sources"].items()}
    need(actual == expected, "Executed source tree mismatch")
    need(owner["pid"] == post["pid"] and owner["token"].startswith(f"{folder.name}/{post['pid']}/"),
         "Child owner mismatch")
    need(post["sourceMatches"] == len(expected) and post["protectedMatches"] == 18
         and not any(post[key] for key in ("terminationFailure", "postflightFailures", "explicitStop"))
         and all(val >= 40_000_000_000 for rec in (post, admission) for val in rec["callerFree"].values()),
         "Postflight or disk mismatch")
    for stream in ("stdout.json", "stderr.txt"):
        need(post[stream] == sha(folder / stream), "Stream identity mismatch")
    if case == "pending":
        need(post["exit"] == 1 and not (folder / "stdout.json").stat().st_size
             and "Selected marker did not run on the resumed ContentManager worker"
             in (folder / "stderr.txt").read_text(), "Pending refusal differs")
    else:
        out = load(folder / "stdout.json")
        stages = {}
        for row in out["packets"]:
            stages.setdefault(row["packet"], []).append(row)
        need(post["exit"] == 0 and not (folder / "stderr.txt").stat().st_size
             and out["native_joins"] == 6 and out["call_restored"] and out["case"] == case
             and out["exe_sha256"] == load(PROTECTION)["protected"][0]["sha256"]
             and len(stages) == (2 if case == "normal" else 1)
             and all([r["stage"] for r in rows] == ["published", "entered", "returned"]
                     and {k: v for k, v in rows[1].items() if k != "stage"}
                     == {k: v for k, v in rows[2].items() if k != "stage"} for rows in stages.values())
             and len({row["pool"] for row in out["packets"] + out["claims"]}) == 1,
             "Native marker evidence differs")
        if case == "normal":
            need([(row["site"], row["marker"]) for row in out["claims"]] ==
                 [("content", 1), ("procgen", 2)] and out["terminal_states"] == [1, 1], "Normal differs")
        else:
            gate = out["gate"]
            need(out["terminal_states"] == [1, 9] and out["claims"][0]["marker"] == 1
                 and gate["held"] == gate["cancelled_return"] and gate["held"]["state"] == 9
                 and gate["held"]["receiver_lock_words"] == [0, 0] and gate["cancel"]["from"] == "held"
                 and "eligible workers quiescent and queues empty" in out["control_stop"], "Missing differs")
    return {"case": case, "class": RESULTS[case], "exit": post["exit"],
            "records": {name: pins(folder / name) for name in
                        ("admission.json", "owner.json", "stdout.json", "stderr.txt", "postflight.json")}}


def earlier_attempts():
    reconcile = load(LOCAL / "reconcile-20261110.stdout.json")
    resume = LOCAL / "resume"
    results = {}
    for row in reconcile["native_attempts"]:
        name = row["name"]
        if name == "native-keys01":
            folder = resume
            files = {key: folder / f"{name}{suffix}" for key, suffix in (
                ("admission_sha256", "-admission.json"), ("postflight_sha256", "-postflight.json"),
                ("stdout", ".stdout.json"), ("stderr", ".stderr.txt"))}
            source, status = folder / "data-source01", folder / f"{name}.exit.txt"
        else:
            folder = resume / name
            files = {key: folder / filename for key, filename in (
                ("admission_sha256", "admission.json"), ("postflight_sha256", "postflight.json"),
                ("stdout", "stdout.json"), ("stderr", "stderr.txt"))}
            source, status = folder / "source", folder / "exit.txt"
        need(all(sha(path) == row[key] for key, path in files.items())
             and all(sha(source / path) == expected for path, expected in row["overlay"].items())
             and int(status.read_text(encoding="utf-8-sig").strip()) == row["code"], f"Earlier attempt differs: {name}")
        results[name] = {"exit": row["code"], "overlay": row["overlay"],
                         "records": {path.as_posix(): pins(path) for path in (*files.values(), status)}}
    prechild = resume / "native-server01"
    need(not (prechild / "admission.json").exists(), "Unexpected pre-child admission")
    results[prechild.name] = {"class": "REFUSED BEFORE ADMISSION", "records": {
        path.as_posix(): pins(path) for path in prechild.iterdir() if path.is_file()
    }}
    return results


def inventory(full):
    need(Path(git("rev-parse", "--show-toplevel")).resolve() == ROOT, "Run at the repository root")
    r3 = load(R3)
    permit = load(PUMP_PERMIT)
    tags_permit = load(TAGS_PERMIT)
    for record in (permit, tags_permit):
        need(record["reviewManifest"] == sha(R3) and record["reviewReport"] == sha(REVIEW)
             and record["protected"] == sha(PROTECTION), "Review or protection pin mismatch")
        for path, digest in record["sources"].items():
            need(sha(Path(path)) == digest, f"Current source differs from reviewed input: {path}")
    work = {row["path"]: pins(Path(row["path"])) for row in r3["files"]}
    need(all(work[row["path"]] == {k: row[k] for k in ("bytes", "sha256")} for row in r3["files"]),
         "Current D5BM path differs from the reviewed checkpoint")
    for path, digest in r3["receipts"].items():
        need(sha(Path(path)) == digest, f"Review evidence differs: {path}")
    for row in r3["patches"].values():
        need(sha(Path(row["path"])) == row["sha256"], "Old patch differs")
    need({p.name for p in ATTEMPTS.iterdir()} == ATTEMPT_CASES.keys(), "Unexpected attempt inventory")
    attempts = {name: r3_attempt(ATTEMPTS / name, case, permit) for name, case in ATTEMPT_CASES.items()}
    refused = {}
    for attempt, filename, missing in (
        ("r3-pump-normal01", "r3-review-pump.json", "vcruntime140.dll"),
        ("r3-pump-normal02", "r3-review-pump-normalized.json", "DLLs/_bz2.pyd"),
    ):
        path = LOCAL / filename
        old = load(path)
        need(missing not in old["runtime"] and missing in permit["runtime"]
             and {key.lower(): val for key, val in old["runtime"].items()} ==
                 {key.lower(): val for key, val in permit["runtime"].items()}
             and all(old[key] == val for key, val in permit.items() if key != "runtime"),
             "Pre-child permit differs beyond its dictionary spelling")
        refused[attempt] = {"class": "REFUSED BEFORE CHILD", "permit": {filename: pins(path)},
                            "unmatched_literal_key": missing, "stream": "session record only"}
    backup = load(Path(".local-work/d5bl/inventory.json"))
    for row in backup["members"]:
        expected = {k: row[k] for k in ("bytes", "sha256")}
        need(pins(Path(row["source"])) == expected
             and pins(Path(".local-work/d5bl") / row["destination"]) == expected,
             f"D5BL custody differs: {row['source']}")
    assets = {}
    for label, family, basename in (
        ("D5AS", "d5be", "d5as-feynman-geometry-v1.zip"),
        ("D5BI", "d5bi", "SOR-D5BI-N2-projected-evidence-v1.zip"),
    ):
        row, = [r for r in backup["members"] if r["family"] == family and Path(r["source"]).name == basename]
        path = Path(row["source"])
        with zipfile.ZipFile(path) as archive:
            need(archive.testzip() is None, "Corrupt candidate archive")
            members = {}
            for item in archive.infolist():
                if not item.is_dir():
                    need(item.filename not in members, "Duplicate candidate archive member")
                    with archive.open(item) as stream:
                        members[item.filename] = {"bytes": item.file_size,
                                                 "sha256": hashlib.file_digest(stream, "sha256").hexdigest()}
        if label == "D5AS":
            expected = load(Path("docs/audits/evidence-access-d5be/d5as-manifest.json"))["asset"]
            expected_members = expected["members"]
        else:
            manifest = load(Path("docs/audits/evidence-derivative-d5bi/manifest.json"))
            expected, expected_members = manifest["candidate"], manifest["members"]
        need(pins(path) == {k: expected[k] for k in ("bytes", "sha256")}
             and all(members.get(key) == pin for key, pin in expected_members.items()), "Candidate manifest differs")
        assets[label] = {"name": path.name, **pins(path), "members": members, "access": "LOCAL / HELD"}
    result = {
        "schema": "sor-d5bn-evidence-inventory/1", "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}"),
        "index_sha256": sha(Path(git("rev-parse", "--git-path", "index"))),
        "staged_paths": git("diff", "--cached", "--name-only").splitlines(),
        "r3_manifest": pins(R3), "r3_review": pins(REVIEW), "d5bm_current": work,
        "r3_attempts": attempts, "r3_permits": {p.name: pins(p) for p in (PUMP_PERMIT, TAGS_PERMIT)},
        "r3_prechild_refusals": refused, "earlier_native_attempts": earlier_attempts(),
        "historical_protection": {"inventory": pins(PROTECTION), "entries": 18},
        "d5bl": {"files": backup["count"], "bytes": backup["bytes"], "original_and_copy_verified": True},
        "local_assets": assets,
        "unrun": ["injected controller fault", "BIOM tag-map fixture", "shared-host Stage A", "Stage B"],
        "missing_or_unknown": ["pending stdout events", "pre-child refusal streams outside the session record",
                               "exact-final D5BJ receipts", "security trigger and feedback disposition"],
    }
    if full:
        result["ignored_d5bm_files"] = dict(full_members(LOCAL))
        result["worktree_status"] = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    print(json.dumps(inventory(parser.parse_args().full), indent=2, sort_keys=True))
