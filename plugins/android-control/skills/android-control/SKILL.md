---
name: android-control
description: "安卓控制：操作真实安卓手机，管理应用、界面、文件与连接。 Use ADB, app interfaces, and UI automation for authorized work on an identified physical Android phone; verify device identity and phone-side results."
---

# 安卓控制 · android-control

Extend the user's reach to the phone while keeping the phone's own state in
view. The host is a hand and a window: it can act at a distance, but a successful
gesture on the host matters only when the intended phone responds.

The user supplies the task and its authorization; the model connects that
purpose to one identified physical device and the relevant app or files. ADB
transport aliases identify connections, not necessarily different phones.
App hierarchies expose controls, while overlays and transitions can change what
a gesture reaches. Login and permission decisions retain their actual owners.
These relations make device identity, fresh observation, and phone-side
readback part of the operation rather than optional diagnostics.

Complete the requested task through the current connection. Reuse established
access and authorization, select ADB, app-native interfaces, or UI automation
for the operation, and verify its effect on the identified phone. A terminal
command is not automatically a better interface.

## Connect and inspect

Bind the connection to the device before binding a gesture to a control:

1. Run `python3 <skill>/scripts/android_inspect.py devices`. It reports ADB
   transport names and physical identities. Multiple mDNS aliases can represent
   one phone; compare identities before treating them as separate devices.
   Select an explicit current serial for subsequent commands. Resolve ambiguity
   from task context or the user before a mutation on an unidentified phone.
2. For UI work, use the compact package-filtered snapshot:

   ```bash
   uv run --no-project --with uiautomator2 python \
     <skill>/scripts/android_inspect.py ui --serial "$ANDROID_SERIAL" \
     --package com.android.settings
   ```

   `<skill>` is this installed Skill directory, not the repository source.
   Use a compatible uiautomator2 version in an isolated environment; record the
   version used when reproducibility matters. The helper keeps hierarchy links,
   labels, hints, bounds, and control state. Other packages expose only overlay geometry.
   It masks password nodes and common token forms; treat all output as private
   and inspect the requested app only. This is not a general secret detector.
3. Use fresh observed selectors or bounds with `uiautomator2.connect(serial)`,
   or `adb -s "$ANDROID_SERIAL" …`. Read the state after app transitions and
   actions. When the result is uncertain, inspect before retrying. Screenshots
   help when a hierarchy cannot explain a visible control or overlay.

Read [connection setup and operation recipes](references/phone-environment.md)
for USB/wireless access, installation, temporary screen settings, and UI recovery.
Use the recipient's available tools and existing permissions; this package does
not assume an operating system, phone model, app roster, or credential store.

The helper requires Python 3.9+ and `adb` on PATH for inventory; UI inspection
also requires uiautomator2. `uv` is optional. Commands accept `--timeout` (default
20 seconds) to bound each ADB request or the entire UI inspection subprocess.
Never treat masked output as safe for publication: identifiers, ordinary labels,
and unrecognized secrets can remain.

## Operate and verify

- Keep the identified phone awake throughout sustained UI work, including
  reading and reasoning between gestures. Before the first UI operation, record
  the original display timeout in task continuity, then disable automatic sleep
  through a supported setting. A finite timeout must cover the actual session,
  including pauses between gestures. If the phone exposes only a finite maximum, use a duration that
  covers the work, verify the effective power state and any policy override,
  and describe that limit accurately. Treat this as a task-only override: after
  all phone operations finish, or when phone work is abandoned, restore the
  recorded original value and verify the readback. A context reset or pause
  within ongoing phone work does not complete that work; retain the original
  value until restoration. The setup reference explains effective power-state
  checks and restoration readback.
- Inspect before changing: current package/version, relevant setting, target
  files, and connection state. For directory inspection, prefer a bounded
  listing of the task path (`adb … shell ls -la <path>`) and expand only useful
  branches. Use app export or documented interfaces when they preserve meaning
  more reliably than UI repetition. Verify remote shell quoting for filenames;
  local argument arrays do not remove Android shell interpretation.
- For installs, establish the official source and correct package, build,
  architecture, and signature compatibility. Install through available ADB or
  the configured app manager, then read package/version and actual app startup.
  If an installed VPN, firewall, or proxy scopes access by app,
  inspect the relevant policy within the task and verify an in-app request.
- Prefer semantic selectors; inspect parent/child relationships for switches.
  Flutter labels may be on `content-desc`, while empty inputs only have `hint`.
  Focus an input before sending text and verify persistence after leaving and
  reopening its page. A tap or a successful command alone is not acceptance.
- Use Shizuku/rish only for an operation requiring their shell access. Preserve
  login, personal verification, deletion, and authorization boundaries. The
  Skill itself does not grant device access or approve new permissions.
- If ADB disappears, refresh `adb devices -l` and `adb mdns services`; wireless
  endpoints can change. Recover available access before handing work back.
  Distinguish an unreachable ADB endpoint from failure of Shizuku or the app.

## Keep useful work reusable

Use the bundled inspection helper before writing another XML dump/parser.
Prototype new operations in task-local scratch space. When an operation is
repeated, fragile, or costly to rediscover, consider retaining a small script
or app-specific recipe with the affected project's maintenance owner.
Parameterize device, package, and task paths; use observed selectors and explicit
preconditions, and verify the outcome. Keep one-off coordinates, expiring ports,
tokens, private UI dumps, screenshots, downloaded APKs, and task logs out of the
package. Remove exact temporary files created by the task after validation.
Do not turn a single successful interaction into a scheduler or a general
automation framework without a current need.
