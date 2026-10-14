# Connection setup and operation recipes

Use current device evidence rather than a saved model, address, app list, or
desired-state template. Commands below use an explicitly selected
`ANDROID_SERIAL`; replace example paths and packages with the actual task target.

## Prepare access

Install Android SDK Platform-Tools from the [official Android distribution](https://developer.android.com/tools/releases/platform-tools)
and ensure `adb` is on PATH. Python 3.9+ runs the inventory helper without
third-party Python dependencies. For UI work, install uiautomator2 in a virtual
environment, or use optional `uv run --no-project --with uiautomator2 python ...`.
Follow [uiautomator2's upstream setup](https://github.com/openatx/uiautomator2)
for the selected device and record a compatible version when needed.

On the phone, enable Developer options and USB debugging through its actual
settings. Connect a data-capable USB cable, inspect `adb devices -l`, and complete
any device-owned trust prompt within existing authorization. An `unauthorized`
row is not usable access; `offline` is a transport problem. Do not change broader
security settings just to bypass an installation or trust failure.

For supported wireless debugging, use the phone's current pairing page and
`adb pair HOST:PAIRING_PORT`, then `adb connect HOST:CONNECT_PORT`. Pairing and
connection ports can differ and change. `adb mdns services` helps discover current
services. Compare physical identities using the helper's inventory before
treating multiple transport aliases as different phones. A reported identity
may be absent or insufficient: use task context and phone-side observation to
resolve ambiguity before mutation.

## Inspect and operate

```bash
python3 <skill>/scripts/android_inspect.py devices --timeout 20
python3 <skill>/scripts/android_inspect.py ui --serial "$ANDROID_SERIAL" --package com.android.settings --timeout 20
adb -s "$ANDROID_SERIAL" shell getprop ro.product.cpu.abi
adb -s "$ANDROID_SERIAL" shell dumpsys package com.example.app
```

The UI command needs uiautomator2 in the same Python environment. Each ADB
request is bounded separately; inventory duration can grow with device count.
The UI command bounds connection and hierarchy retrieval together in a child
process. A timeout does not prove a phone-side action failed. The helper only
inspects; it does not tap controls, install apps, or alter settings.

After transitions, wait for the intended activity/control with a finite deadline
and refresh the hierarchy. Prefer semantic selectors and actual switch state.
A Flutter input may expose only `hint`; focus the observed input before sending
text and reopen the page to verify persistence. Handle secret input through the
recipient's approved secret route without echoing values or retaining clipboard
copies. Password labels and recognized token forms are masked, but ordinary
labels and unknown secret formats remain private.

If another app's overlay blocks a control, inspect its geometry without reading
unrelated content. Move or dismiss it only within scope, then restore temporary
changes when appropriate. A screenshot may expose more private content than the
filtered hierarchy; capture only what the task requires.

## Temporary display settings

Before sustained UI work, record the current value:

```bash
adb -s "$ANDROID_SERIAL" shell settings get system screen_off_timeout
adb -s "$ANDROID_SERIAL" shell dumpsys power
```

Choose a supported setting that covers the session, read it back, and check
effective power policy. Some devices accept a large millisecond value such as
`2147483647` (about 24.9 days); this is finite, not a universal sleep-disable
command. Device policy or app overrides can impose a smaller effective limit.
Do not assume zero or minus one means unlimited. If a finite maximum cannot
cover the work, report the actual limit and use supported awake behavior.

Keep the original value in task continuity, restore it after phone work ends,
and verify both the setting and effective state. Restore absence by deleting a
task-created setting rather than storing the text `null`. A pause during ongoing
work is not restoration; context recovery must retain the original value.

## Install and verify an app

Establish an official APK source, package, ABI/build, and signature compatibility.
Inspect the installed package first, then use an authorized installer, for example:

```bash
adb -s "$ANDROID_SERIAL" install -r /actual/task/path/app.apk
adb -s "$ANDROID_SERIAL" shell dumpsys package com.example.app
```

Read package/version and verify real startup. Installation success alone does
not prove login, network access, or background operation. Inspect a relevant
VPN/firewall allowlist if the actual environment uses one, preserve its running
state, and test a real app request. A configured update interval is not evidence
that a scheduled update ran. Avoid competing update managers for one package
unless their responsibilities are deliberately compatible.

## Files and optional shell bridges

Use bounded listings at the actual task path. For transfer, `adb -s SERIAL push`
and `pull` are usually clearer than typing a long shell command. Verify remote
shell quoting; local argument arrays do not remove Android shell interpretation.
Confirm resulting file size/content or the app's imported result as appropriate.
Clean up only exact task-created temporary files.

Shizuku, rish, and Termux are optional, not dependencies of this package. Use
them only when the actual operation needs their capabilities; obtain setup
instructions and binaries from their official sources, verify service state,
and preserve their real permission boundaries. Do not assume boot persistence,
root access, a particular terminal build, or a preconfigured installer.
