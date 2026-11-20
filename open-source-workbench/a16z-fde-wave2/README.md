# a16z FDE Open-source Contribution Workbench — Wave 2

Prepared 20 November 2026. This bundle contains three additional Modal client patch proposals grounded in current upstream source and issue descriptions. They are proposed contributions, not submitted or accepted upstream PRs.

## Active candidates

| Project | Issue | Proposed change | Current state |
|---|---|---|---|
| Modal | [#4148](https://github.com/modal-labs/modal-client/issues/4148) | Parse Docker COPY JSON/exec-form sources, preserve paths containing spaces, and normalize COPY ./ | Patch and regression cases prepared; isolated parser matrix passed |
| Modal | [#4151](https://github.com/modal-labs/modal-client/issues/4151) | Normalize automatic .dockerignore rules through the existing Moby-compatible read_ignorefile helper | Patch and upstream integration-test hunk prepared; local parser-contract check passed |
| Modal | [#4149](https://github.com/modal-labs/modal-client/issues/4149) | Normalize relative Dockerfile and context paths before containment checks | Patch and regression test prepared; local pathlib check passed |

## Checked and excluded

- Anthropic skills #2201: matching open PR #2211 was found, so it is excluded to avoid duplicate work.
- Modal #4130: the issue is still open and no matching open PR appeared in the targeted search, but the implementation is held for a separate pass because the correct file-versus-directory destination semantics need a fuller test harness around iterdir() and concurrent downloads.

## Validation

The dependency-free local harness reports 8 isolated checks passed: six Docker COPY forms (including the three issue reproductions and two shell-form controls), one ignore-file normalization case, and one relative-path resolution case. All three patch files parse with git apply --stat.

These results do not establish that the Modal upstream repository's full test suite passes. The Modal pytest suite, live build, remote Volume RPC, and cloud integration tests were not run.

## Submission status

No upstream branch, commit, issue comment, or PR was created by this bundle. The connected GitHub integration can read upstream repositories but does not have upstream push permission, and its issue-comment write action was rejected. The bundle can be reviewed locally and then submitted through an authorized fork/PR workflow.
