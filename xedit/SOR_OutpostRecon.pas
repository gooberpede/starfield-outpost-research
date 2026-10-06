unit SOR_OutpostRecon;
// SPDX-License-Identifier: GPL-3.0-or-later
// Project-authored bounded reader; no plugin writes. See README.md.
// API reference: SOR-S-0103 (Tome of xEdit); no example script adapted.
var
  rows, meta: TStringList;
  stem: string;
  seen, matched, detailed, leaves: integer;

function Cell(s: string): string;
begin
  s := StringReplace(s, #9, ' ', [rfReplaceAll]);
  s := StringReplace(s, #13, ' ', [rfReplaceAll]);
  Result := StringReplace(s, #10, ' ', [rfReplaceAll]);
end;

function Relevant(s: string): boolean;
begin
  s := LowerCase(s);
  Result := (Pos('outpost', s) > 0) or (Pos('workshop', s) > 0)
    or (Pos('cargolink', s) > 0) or (Pos('harvester', s) > 0)
    or (Pos('extractor', s) > 0) or (Pos('fabricator', s) > 0)
    or (Pos('resourcelink', s) > 0);
end;

procedure Fields(e: IInterface; prefix, location: string; depth: integer);
var i: integer; child: IInterface; p: string;
begin
  if (leaves >= 300) or (depth > 10) then begin
    meta.Add('TRUNCATED_FIELDS' + #9 + prefix + #9 + location);
    exit;
  end;
  if ElementCount(e) = 0 then begin
    rows.Add(prefix + #9 + Cell(location) + #9 + Cell(GetEditValue(e)));
    Inc(leaves);
    exit;
  end;
  for i := 0 to ElementCount(e) - 1 do begin
    if leaves >= 300 then begin
      meta.Add('TRUNCATED_FIELDS' + #9 + prefix);
      exit;
    end;
    child := ElementByIndex(e, i);
    p := location + '/' + IntToStr(i) + ':' + Name(child);
    Fields(child, prefix, p, depth + 1);
  end;
end;

function Initialize: integer;
var i: integer;
begin
  Result := 0;
  rows := TStringList.Create;
  meta := TStringList.Create;
  stem := 'D:\Projects\starfield-outpost-research\.local-work\recon\xedit-' + FormatDateTime('yyyymmdd-hhnnss', Now);
  if FileExists(stem + '.tsv') or FileExists(stem + '-meta.txt') then begin
    AddMessage('SOR: output exists; aborting without overwriting.');
    Result := 1;
    exit;
  end;
  rows.Add('plugin' + #9 + 'file_formid' + #9 + 'session_formid' + #9 + 'signature' + #9 + 'editorid' + #9 + 'path' + #9 + 'value');
  meta.Add('schema=SOR-recon-1; local-only; generated=' + DateTimeToStr(Now));
  meta.Add('xEdit=' + wbAppName + '; versionNumber=' + IntToStr(wbVersionNumber));
  meta.Add('Selection: operator-selected records; filters in SOR_OutpostRecon.pas; not an exhaustive map.');
  for i := 0 to FileCount - 1 do meta.Add('loaded=' + GetFileName(FileByIndex(i)));
end;

function Process(e: IInterface): integer;
var sig, ed, prefix: string;
begin
  Result := 0;
  sig := Signature(e);
  if Pos('|' + sig + '|', '|ACTI|AVIF|COBJ|CONT|FLST|FURN|GLOB|KYWD|MISC|NPC_|PACK|QUST|RSPJ|SCOL|STAT|GBFM|') = 0 then exit;
  Inc(seen);
  ed := EditorID(e);
  if not Relevant(ed) then exit;
  Inc(matched);
  if matched > 3000 then exit;
  prefix := Cell(GetFileName(GetFile(e))) + #9 + IntToHex(FormID(e), 8) + #9 + IntToHex(GetLoadOrderFormID(e), 8) + #9 + sig + #9 + Cell(ed);
  rows.Add(prefix + #9 + '@record' + #9 + Cell(Name(e)));
  // Detail only core definitions; COBJ/STAT/SCOL inventories remain identifiers.
  if (detailed < 120) and (Pos('|' + sig + '|', '|ACTI|AVIF|CONT|FLST|GLOB|KYWD|QUST|') > 0) then begin
    Inc(detailed);
    leaves := 0;
    Fields(e, prefix, '', 0);
  end;
end;

function Finalize: integer;
begin
  Result := 0;
  meta.Add('seen=' + IntToStr(seen) + '; matched=' + IntToStr(matched) + '; detailed=' + IntToStr(detailed));
  if matched > 3000 then meta.Add('TRUNCATED_RECORDS=3000');
  if detailed >= 120 then meta.Add('DETAIL_LIMIT_REACHED=120');
  rows.SaveToFile(stem + '.tsv');
  meta.SaveToFile(stem + '-meta.txt');
  AddMessage('SOR output: ' + stem + '.tsv and -meta.txt');
  rows.Free;
  meta.Free;
end;

end.
