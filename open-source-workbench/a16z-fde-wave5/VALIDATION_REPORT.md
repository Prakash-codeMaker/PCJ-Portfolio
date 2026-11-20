# Wave 5 validation report

## Issue and duplicate check

- Modal client issue #4130 remains open.
- Targeted open-PR search for #4130 returned no matching open PR.
- The issue reproduction and source pointer match py/modal/cli/_download.py on the current default branch.

## Source inspection

- py/modal/cli/_download.py blob: 4c7fb6f1ac357e7256ea9abb677f669bc259b2b7.
- py/modal/volume.py blob: dc343773c2ae3ae342e644cb21b54e67c5dff756.
- py/test/volume_test.py blob: 694ea693f202d53fc86e71e6270e1e221ed87d91.
- Historical introduction commit 70715019da0da6ac0c400ee4924158d351750062 changed output mapping to depend on local_destination.is_dir(), enabling a new local filename for a single remote file but leaving the remote-directory/nonexistent-destination case untested.

## Local validation

- path_contract_tests.py: 8 checks passed for new-directory child paths, nested directories, renamed single files, single files inside existing directories, root directory records, rejecting file destinations for directories, and rejecting entries outside the requested path.
- git apply --stat parsed the patch as two files changed: _download.py and volume_test.py.

## Not validated

- The patch was not applied to a complete upstream checkout; git apply --stat validates patch parsing, not clean application.
- The proposed async integration test was not executed against Modal's servicer.
- Full Modal pytest suite and live Volume RPCs were not run.
- Empty remote directories and symlink downloads remain outside the regression case.
- No upstream branch, issue comment, or PR was created.
