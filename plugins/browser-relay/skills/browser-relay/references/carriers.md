# Bind a real carrier

The private-origin runtime integrated a dedicated authenticated owner, a separate
headless carrier, target pinning and desktop placement. Those integrations are
not portable merely by deleting paths. This public package keeps their contract
and explicitly requires a recipient-configured carrier. No `auth-*` command,
private connector resource or pre-existing signed-in profile is provided.

## Recipient-owned configuration

Keep these bindings with the recipient's existing host/project owner. Read that
configuration and current tool documentation rather than inventing another
registry or filling the public package with account/profile data.

| Binding | What current evidence must establish |
| --- | --- |
| Carrier and API | Actual installed tool/provider, documented create/attach, inspect, navigate, act and lifecycle operations. |
| Target ownership | Task-created page handle, or original retained binding checked against the current exact target. URL/title similarity alone is insufficient. |
| Authentication owner | Dedicated authorized context/profile and observed intended account, when needed. Do not discover/export daily-browser cookies or copy profiles. |
| Lifecycle | Whether release retains a pinned target, close retires it, and owner shutdown would affect other targets. Bind available operations to these meanings; they are not invented API names. |
| Placement policy | Current working display/window evidence and real background/non-activating or separate-display support for visible work. |
| Credential owner | Recipient's actual credential/authentication route and personal-consent boundary. The package never supplies a secret or access grant. |
| Continuation evidence | Exact carrier/target binding and meaningful readback for the same task, held in the existing task owner. Exclude session tokens and sensitive content from public logs. |

Validate a harmless task-owned page before using a newly configured carrier:
create it, inspect a known destination/content, perform a reversible action,
read its effect, close or release according to the selected lifecycle, and
verify that effect through the carrier's inventory/handle. Test actual placement
separately when visible work is required. A passing headless test does not prove
authenticated ownership, account identity, multi-display placement or retention.

## Concrete standard route for ephemeral headless work

[Playwright](https://playwright.dev/python/docs/intro) supplies real browser,
context and page APIs. A task-created non-persistent context keeps unrelated
browser sessions outside the operation; the live Page object is process-local
ownership evidence. Its [`BrowserContext`](https://playwright.dev/python/docs/api/class-browsercontext)
and [`BrowserType`](https://playwright.dev/python/docs/api/class-browsertype)
documentation defines creation, persistent contexts and closure. Use the host's
supported browser tool instead when it already provides the necessary capability.
No Playwright dependency is required for such a native host carrier.

For the optional bundled smoke example, install Python 3.10+ and Playwright in
a virtual environment, then install its Chromium runtime as described in
[README.md](../README.md). [Browser installation](https://playwright.dev/python/docs/browsers)
is a separate dependency step. The example uses local fixture content, no network,
authentication or existing profile. It is a verification example, not a general
browser controller or an authenticated relay installation.

For persistent authenticated contexts, a recipient can configure the documented
`launch_persistent_context(user_data_dir=...)` route with a dedicated approved
directory and lifecycle owner. Do not supply the recipient's daily profile or
assume that a path implies a valid session. Its context closure can retire the
whole launched browser, so it cannot stand in for a task-page release operation
when other users/tasks share that owner. A retained shared owner instead needs
its own actual supported attach/release operations and exact-target evidence.
Do not concurrently launch the same profile or recreate an unreachable active
owner. Preserve the browser's credential authority and account through recovery.

## Conditional source companions

The local source names `chrome-configuration` for browser settings/extensions
and `jev-browser-use` for selected delegated browser loops. These are separate
method owners, not transport APIs. This package does not bundle or assume public
versions of them. Use them when actually installed under the task's authority,
or the recipient's corresponding configuration/loop method. Ordinary Relay
operations need neither. A caller such as [paper-retrieval](../../paper-retrieval/SKILL.md)
can compose this custody method with domain-specific byte/version verification;
Relay does not select the papers or certify their completeness.
