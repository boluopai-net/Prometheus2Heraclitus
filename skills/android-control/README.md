# 安卓控制 · android-control

[中文指南](README.zh-CN.md)

Operate an identified real Android phone from the current host: inspect its UI
and files, manage apps, recover connections, and verify results on the device.
This is an operations Skill, rather than an Android application development kit.
It works independently of any particular desktop, phone, app roster, or account.

## Use and dependencies

Copy this complete directory into a Skill location supported by your agent host.
The model-facing `SKILL.md` describes the method; the helper and recipes remain
inside the package. The agent needs appropriate command/device access and the
task's existing authorization. This package grants no permissions.

Inventory needs Python 3.9+ and Android SDK Platform-Tools (`adb`) on PATH.
UI inspection additionally needs [uiautomator2](https://github.com/openatx/uiautomator2)
in the same Python environment. A virtual environment is suitable; [uv](https://docs.astral.sh/uv/)
is an optional alternative. Actual phone-side debugging/trust setup is described
in [connection setup and recipes](references/phone-environment.md).
Installation and UI gestures require tools the recipient actually has.

Example request: “On the connected phone, inspect Example App's Wi-Fi-only update
switch, enable it, reopen the page, and verify that it stayed enabled.”
The agent inventories transport aliases, identifies the intended physical device,
uses fresh controls, performs the scoped action, and reads back persistence.

```bash
python3 scripts/android_inspect.py devices --timeout 20
uv run --no-project --with uiautomator2 python scripts/android_inspect.py ui --serial SERIAL --package com.example.app --timeout 20
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The helper emits compact JSON and performs read-only inspection. The tests use
mocks and require neither a device nor adb/uiautomator2. Each ADB request has its
own deadline; UI connection plus hierarchy retrieval share a bounded subprocess.
Password nodes and common token labels are masked; output can still contain
device identifiers, private labels, and unrecognized secrets. Keep it private.

## Package and adaptation

The English method, setup reference, helper, mock tests, optional agent metadata,
and aligned README editions form the complete package. This public adaptation
retains the original local Skill's device identity, scoped inspection, readback,
temporary-setting restoration, and privacy methods. It replaces owner-specific
phone/app/account observations with portable setup and recipes, and adds a UI
inspection deadline. No private device records or credentials are included.

This independent package uses the [MIT License](LICENSE). Upstream dependencies
retain their own licenses; no upstream binaries are bundled.
