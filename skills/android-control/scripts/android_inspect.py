"""Read-only ADB inventory and compact, package-scoped UI inspection."""

import argparse
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


ADB_TIMEOUT = 20


def adb(*args):
    return subprocess.check_output(
        ["adb", *args], text=True, timeout=ADB_TIMEOUT, stderr=subprocess.PIPE
    ).strip()


def devices():
    result = []
    for line in adb("devices", "-l").splitlines()[1:]:
        # mDNS serials can contain spaces, e.g. "… (2)._adb-tls-connect._tcp".
        match = re.match(r"^(.+?)\s+(device|offline|unauthorized)(?:\s|$)", line)
        if not match:
            continue
        serial, state = match.groups()
        entry = {"serial": serial, "state": state}
        if state == "device":
            for key, prop in (
                ("identity", "ro.serialno"),
                ("model", "ro.product.model"),
                ("android", "ro.build.version.release"),
            ):
                try:
                    entry[key] = adb("-s", serial, "shell", "getprop", prop)
                except (subprocess.SubprocessError, OSError):
                    entry[key] = None
        result.append(entry)
    return result


def safe_label(value):
    return re.sub(
        r"(?:github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]+|"
        r"Bearer\s+[A-Za-z0-9._~+/=-]+)",
        "[REDACTED]",
        value,
        flags=re.IGNORECASE,
    )


def compact_ui(xml, package):
    nodes, overlays = [], set()

    def visit(element, parent=None, masked=False, parent_owner=""):
        attrs = element.attrib
        masked = masked or attrs.get("password") == "true"
        owner = attrs.get("package", "")
        next_parent = parent
        if owner == package:
            node = {"id": len(nodes), "parent": parent}
            for key in ("class", "resource-id", "bounds"):
                if attrs.get(key):
                    node[key] = attrs[key]
            for key in ("text", "content-desc", "hint"):
                if attrs.get(key):
                    node[key] = "[REDACTED]" if masked else safe_label(attrs[key])
            for key in (
                "clickable",
                "checkable",
                "checked",
                "scrollable",
                "focused",
                "enabled",
                "password",
            ):
                if key in attrs:
                    node[key] = attrs[key] == "true"
            next_parent = node["id"]
            nodes.append(node)
        elif owner and owner != parent_owner and attrs.get("bounds"):
            overlays.add((owner, attrs["bounds"]))
        for child in element:
            visit(child, next_parent, masked, owner)

    visit(ET.fromstring(xml))
    return {
        "package": package,
        "nodes": nodes,
        "other_windows": [
            {"package": owner, "bounds": bounds} for owner, bounds in sorted(overlays)
        ],
    }


def inspect_ui(serial, package, timeout):
    # Isolate the library connection as well as hierarchy retrieval under one
    # deadline. Capture stderr: dependency failures can include remote output.
    worker = (
        "import sys,uiautomator2 as u2; "
        "sys.stdout.write(u2.connect(sys.argv[1]).dump_hierarchy())"
    )
    xml = subprocess.check_output(
        [sys.executable, "-c", worker, serial],
        text=True, timeout=timeout, stderr=subprocess.PIPE
    )
    result = compact_ui(xml, package)
    result["serial"] = serial
    return result


def positive_timeout(value):
    seconds = float(value)
    if not 0 < seconds <= 300:
        raise argparse.ArgumentTypeError("timeout must be greater than 0 and at most 300")
    return seconds


def main():
    global ADB_TIMEOUT
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("devices")
    inventory.add_argument("--timeout", type=positive_timeout, default=20)
    ui = commands.add_parser("ui")
    ui.add_argument("--timeout", type=positive_timeout, default=20)
    ui.add_argument("--serial", required=True)
    ui.add_argument("--package", required=True)
    args = parser.parse_args()
    ADB_TIMEOUT = args.timeout
    try:
        if args.command == "devices":
            result = devices()
        else:
            result = inspect_ui(args.serial, args.package, args.timeout)
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    except Exception as exc:
        # Exception messages can contain private XML/remote output.
        parser.exit(
            1, f"Inspection failed ({type(exc).__name__}); check connection and dependencies.\n"
        )


if __name__ == "__main__":
    main()
