---
name: browser-relay
description: "<用户自制> 浏览器会话：管理任务专用的隔离浏览器、授权登录会话与清理。 Hold exact physical target custody for bounded authenticated, in-app or headless browser operations; verify destination, effects, session boundaries and lifecycle."
user-invocable: false
---

# browser-relay

A browser operation visits an exact place in a world already occupied by people,
sessions and unfinished work. A responsible visit has a purpose, an address,
observable effects and an accounted departure or continuation. Preserve the
surrounding work as the task reaches into it.

Access, custody and authority differ. The caller owns purpose, authorized effects,
success criteria and use of the result. Browser Relay holds custody of the exact
physical target: positive ownership, destination verification, operation readback
and cleanup evidence. A URL tells where to go; an owned handle or verified carrier
binding establishes which target may be controlled. Connect each action to its
observed effect at that same target.

For a model-message exchange, the caller also owns exchange identity, semantic
binding, response completion and wait/retry decisions. The physical relay returns
what happened at the page. It does not become the conversation or research owner.

## Enter and bind the operation

Use this relay when a bounded operation needs a controlled browser carrier,
including authenticated model-conversation work or a task-owned headless page.
Select and bind an available carrier through [carrier configuration](references/carriers.md)
under the host's actual browser, daily-session, authorization and desktop policy.
Use current documented operations and returned handles; the recipient supplies
the installed browser owner and its APIs.

The caller supplies the destination or retained binding, bounded operation,
authorized effects, relevant prior state, expected readback and lifecycle:
close an ephemeral target, release control while retaining an authorized session
or page, or retire an exact owned target. Resolve routine details from evidence
within that scope. For a message operation, additionally bind `observe` or `submit`,
the last known message boundary and exact payload for `submit`.

| Operation and host route | Carrier and lifecycle |
| --- | --- |
| In-app browser selected by host policy | Create an owned tab; close it after the operation unless retained for a same-task continuation. |
| Signed-in work in a dedicated authorized context | Acquire an exact owned page, use page-bound controls, and release control while retaining the page when declared; close that page when retiring it. |
| Unauthenticated headless work | Create an isolated context and owned page; close both after the operation. |

The [carrier lifecycle](#carrier-lifecycle) section defines the ownership,
retention, and closure evidence for each route.

When browser settings, policies, extensions or options are the task object, retain
their separate configuration owner (`chrome-configuration` in the local source).
An explicitly authorized daily-browser settings target does not authorize using
its unrelated sessions. If the host selects a delegated browser loop, the source's
`jev-browser-use` companion can supply that loop when actually installed; Relay
still owns the exact target and cleanup. These are conditional method relationships,
not prerequisites for an ordinary owned-page operation. See [dependencies](README.md).

## Physical operation contract

1. Select the allowed carrier and establish positive ownership of the exact tab
   or page. Keep its returned live handle or verified retained binding. URL equality
   is not ownership; do not claim a pre-existing matching tab.
2. Verify destination and current authentication/challenge state. Inspect the
   relevant page and controls before the bounded action.
3. Perform the authorized navigation, inspection, edit, download, save or other
   operation using current UI/tool evidence. Preserve caller-supplied exact content.
   Refresh targets after changes that invalidate them.
4. Return carrier/target identity, current destination, observations or retrieved
   content, attempted effects and actual persisted readback, unresolved ambiguity,
   and lifecycle evidence. The caller judges semantic adequacy and task completion.
5. In `finally`, perform the declared cleanup and read back its effect. Cleanup
   failure is a physical-operation failure, not authority to adopt another target.

For downloads, bind the returned bytes to the initiating page/action. A shared
browser-wide capture channel needs serialization or a supported unique initiation
identifier matched to completion. Page-local capture may permit independent pages.
Browser completion alone does not verify file identity; the scholarly or other
domain owner supplies that verification.

### Model-message relay

For `observe` or `submit`, preserve the exact conversation and message boundary.
Return ordered observable message IDs/text where available, authentication and
running/paused state, attempted mutations and cleanup evidence. The caller retains
semantic response binding, completion, waiting and retry.

`observe` does not submit, resend, alter the target or wait for semantic completion.
`submit` attempts exact caller bytes once only when not running or paused; otherwise
return busy evidence without submission. Do not rewrite payloads, add attachments,
choose another conversation, decide the answer or initiate another exchange.
An ambiguous submission returns to the caller for reconciliation, never a blind
resend. A visible click is not proof of submission or persistence.

## Carrier lifecycle

**In-app browser.** Use its currently exposed browser/tab API and documentation.
Create one owned tab for the exact operation and retain the live handle. Select
visibility according to the host's actual panel/desktop policy. A separate browser
Skill is not needed when the tool already supplies its interface. Close a task-created
tab at completion/abort and verify absence in a non-creating inventory; retain it
only for a real same-task continuation. Replace a stale handle only when controlled
target evidence proves absence or exact reclamation with original ownership.

**Dedicated authenticated carrier.** Reuse only the configured task-authorized
profile/context and verified account. Isolate tasks through exact owned pages,
not by casually swapping profiles. A missing, corrupt, wrong-account or unreachable
owner requires diagnosis; it does not authorize copying a daily profile, replacing
the owner or changing credential storage. Browser application identity and its OS
credential encryption authority can matter independently of profile directories;
preserve both through an actually authorized migration.

For ordinary authenticated work, acquire a pinned page, operate through its
page-bound controls, then release the task's control in `finally`. Verify that
the same target remains retained when that is the declared lifecycle. Retention
is distinct from closure. Reacquiring a retained page verifies identity, destination
and placement before navigation. Close only the exact task page when retirement
is intended; preserve the profile and other tasks' or recipient-owned pages.
Owner status is read-only; starting an absent owner must not navigate existing
targets. Retire a browser owner only when current evidence establishes no other
dependent task or retained user/login page.

For first-time login or a currently evidenced authentication/challenge boundary,
use the host's authorized bootstrap and credential owner. Complete available
steps without printing or exporting secrets. Actual personal verification and
consent remain with their owners. Preserve account identity during recovery.
Do not infer entitlement from session success.

**Task-owned headless carrier.** For unauthenticated operations create an isolated
context and owned page through the configured API. Keep that exact handle through
the bounded action and close the page/context in `finally`, verifying closure.
If attachment already creates a page, do not create another by accident. A missing
or changed target must not be replaced by a default or another task's page.
An unauthenticated context is not authentication authority for a signed-in task.

No watcher, keepalive, sweeper, queue, tab database or dashboard is required by
this method. An optional observer surface is not a second target owner.

## Placement and recovery

Before visible browser work, inspect the actual display/window evidence and bind
the host's placement policy. Preserve the recipient's focus, pointer and occupied
work. Where that policy reserves the working display, place the exact task window
on another physical display without activation and verify the composed result
before page interaction. An occupancy check or unused rectangle does not satisfy
that boundary. If only one display is available, or safe placement cannot be
established, use a supported background/headless route. A browser API must actually
support the requested placement/non-activation behavior; this method cannot
make a foreground-launching carrier safe by declaration.

Resolve carrier, stale-handle, visibility and lifecycle failures within existing
authority. An absent browser, hidden task or queued panel is technical evidence,
not proof that only the user can act. Investigate the exact target and permitted
recovery routes. Read back uncertain effects before any retry; if their outcome
cannot be established, return the ambiguity. Preserve the single-attempt message
submission boundary. Name remaining technical limitations and routes considered.
Request personal participation only for an evidenced authentication, consent or
other actual human-only boundary that available authorized recovery cannot resolve.

## Native scheduled-task editor branch

Use only within the caller's actual task-maintenance authority; browser access
does not grant that authority. Open the exact existing native task/conversation,
inspect its editor and current prompt/enabled state, edit through the current
labelled control, and save through the native save or unsaved-change confirmation.
Reload/reopen the same target and read back exact prompt plus paused/enabled state.
A focused textarea or successful click is not save evidence. Editing alone does
not require resuming a paused task. Control labels are provider-specific; discover
the current interface rather than assume a private service target or fixed URL.

Stop adoption on target mismatch, lost ownership, unresolved login/challenge or
cleanup failure. Return running/paused state and post-mutation ambiguity as
physical observations. The caller retains semantic and authorization decisions.
