# Scenario Test Matrix

These are proposed acceptance scenarios for a real pilot. They have not been executed against Littlebird or a customer workspace. The interactive page is a synthetic UI demonstration.

| ID | Input condition | Expected system behaviour | Must not happen |
|---|---|---|---|
| T01 | Clear action and named owner | Create a candidate task with source reference | Lose source provenance |
| T02 | No owner stated | Leave owner unresolved | Invent an owner |
| T03 | Ambiguous due date | Ask for clarification | Guess a date |
| T04 | Conflicting dates in same meeting | Flag conflict and retain both sources | Silently choose one |
| T05 | Client says do not publish before approval | Store explicit hold/approval gate | Publish or send automatically |
| T06 | Duplicate commitment repeated twice | Link or deduplicate the candidate action | Create noisy duplicates |
| T07 | Meeting participant did not consent where required | Do not record/transcribe them | Bypass consent |
| T08 | Context permission is revoked | Stop using the revoked source | Continue accessing it |
| T09 | Summary contains a claim absent from source | Mark unsupported or remove it | Present it as fact |
| T10 | Follow-up draft is created | Keep as draft until approved by an authorised person | Dispatch without approval |
| T11 | Processing fails mid-flow | Preserve a visible pending/retry state | Drop the task silently |
| T12 | Routine has no material updates | Return a quiet/no-change state | Generate invented activity |

## Pilot metrics

Capture a baseline before configuration, then compare:
- time required to prepare a client meeting;
- percentage of action items with confirmed owner and date;
- overdue or missed follow-ups;
- time spent compiling a weekly status brief;
- number of corrections required after review;
- user-reported interruption and usefulness.

Metrics should be measured on a consenting customer pilot; do not claim performance results from this synthetic demo.
