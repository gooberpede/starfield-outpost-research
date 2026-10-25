-- SPDX-License-Identifier: GPL-3.0-or-later
-- PROPOSED / NOT EFFECTIVE. One logical index per grouping version.
-- This is schema only, with no real production members or trusted root.
-- Reader/writer APIs enforce path, size, alias and external-digest validation.
PRAGMA user_version = 2;
CREATE TABLE archives (
    id TEXT PRIMARY KEY, filename TEXT, format TEXT, digest TEXT,
    bytes INTEGER, grouping_version TEXT
);
CREATE TABLE members (
    archive_id TEXT, path TEXT, digest TEXT, bytes INTEGER,
    original_location TEXT, research_system TEXT,
    PRIMARY KEY (archive_id, path)
);
CREATE TABLE aliases (
    archive_id TEXT, original_location TEXT, member_path TEXT,
    digest TEXT, bytes INTEGER,
    PRIMARY KEY (archive_id, original_location)
);
CREATE TABLE cross_references (
    consumer_system TEXT, original_location TEXT,
    owner_archive TEXT, member_path TEXT
);
