# Open-source contribution workbench — Wave 5

Prepared 20 November 2026. This wave prepares a source-grounded patch for Modal issue #4130, a data-loss bug in the local destination mapping for directory downloads.

## Active target

**Modal client #4130 — modal volume get can corrupt directory downloads when the local destination does not exist**

- Issue: https://github.com/modal-labs/modal-client/issues/4130
- Source inspected: py/modal/cli/_download.py (blob 4c7fb6f1ac357e7256ea9abb677f669bc259b2b7), py/modal/volume.py (blob dc343773c2ae3ae342e644cb21b54e67c5dff756), and py/test/volume_test.py (blob 694ea693f202d53fc86e71e6270e1e221ed87d91).
- Targeted open-PR search found no matching upstream PR.

### Proposed fix

The existing implementation decides whether to append a relative path by checking local_destination.is_dir(). For a remote directory and a destination that does not exist, that check is false for every listed entry, so concurrent workers can all open the same destination path with wb.

The patch adds Volume-specific remote path classification:
- A single remote file keeps the ability to be downloaded to a new filename.
- A file downloaded into an existing local directory retains its basename.
- A remote directory maps each entry relative to the requested remote directory, independent of whether the destination already exists.
- The NetworkFileSystem path (including its glob behavior) remains on the previous code path.
- Entries outside the requested Volume directory and path traversal segments are rejected.

The patch also adds an integration regression test that uploads two files under a remote directory, downloads into a nonexistent path with concurrency 2, and verifies both files and their exact contents.

## Validation performed

- path_contract_tests.py: 8 isolated path-selection checks passed.
- git apply --stat parses the patch.
- The upstream integration test was added to the proposed patch but has not been run against a full Modal checkout.

## Limits

No upstream Modal repository was modified and no upstream PR is claimed. The proposed patch has not been applied to a complete checkout. The full Modal pytest suite, V1/V2 behavior, empty directories, symlink handling, and remote integration need testing before upstream submission.
