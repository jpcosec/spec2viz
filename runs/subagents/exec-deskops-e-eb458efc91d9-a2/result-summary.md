# Result
run_id: exec-deskops-e-eb458efc91d9-a2
session: n/a (claude executor, no child session file); session_sha256: n/a

Changed (committed on branch deskops/deskops-e-eb458efc91d9-a2):
- src/specir/extract/write.py: checked_blocks compares fact source_hash with a fresh sldb.api.code.code_facts of the fact paths; no hashlib/read_bytes. ValueError with ref kept; nothing written if an anchor fails.
- tests/extract/test_blog_extraction.py: new test_the_extractor_reads_no_source_file (spies open/Path.read_bytes/read_text called directly from specir/extract).

Validation: see validation.log. Review: 1 failing test (tables columns order) is pre-existing, reproduced with my src change reverted; likely tree-sitter-sql version in my ad-hoc venv. Note record_anchor (sldb) still reads the source internally, which is sldb's side.
