"""Mock regressions for UI privacy, connection identity, and bounded inspection."""

import unittest
from unittest.mock import patch

import subprocess

from android_inspect import adb, compact_ui, devices, inspect_ui, positive_timeout


class InspectionTests(unittest.TestCase):
    def test_mdns_alias_with_spaces_keeps_same_physical_identity(self):
        inventory = (
            "List of devices attached\n"
            "phone (2)._adb-tls-connect._tcp device model:Example\n"
            "phone._adb-tls-connect._tcp device model:Example"
        )
        with patch("android_inspect.adb", side_effect=[inventory] + ["ID", "Example", "16"] * 2):
            result = devices()
        self.assertEqual(result[0]["serial"], "phone (2)._adb-tls-connect._tcp")
        self.assertEqual(result[0]["identity"], result[1]["identity"])

    def test_flutter_hint_switch_and_overlay_privacy(self):
        xml = """<hierarchy><node package="app" bounds="[0,0][100,100]">
          <node package="app" hint="Token" password="true" text="secret"/>
          <node package="app" content-desc="Wi-Fi only">
            <node package="app" class="android.widget.Switch" checked="true"/>
          </node>
          <node package="app" text="github_pat_abcd_1234"/>
        </node><node package="chat" bounds="[70,0][100,30]" text="private">
          <node package="chat" bounds="[70,0][80,20]" text="message"/>
        </node></hierarchy>"""
        result = compact_ui(xml, "app")
        self.assertEqual(result["nodes"][1]["text"], "[REDACTED]")
        self.assertTrue(result["nodes"][3]["checked"])
        self.assertEqual(result["nodes"][3]["parent"], 2)
        self.assertEqual(result["nodes"][4]["text"], "[REDACTED]")
        self.assertEqual(result["other_windows"], [{"package": "chat", "bounds": "[70,0][100,30]"}])
        self.assertNotIn("private", str(result))
        self.assertNotIn("message", str(result))

    def test_ui_inspection_deadline_and_explicit_serial(self):
        with patch("android_inspect.subprocess.check_output", return_value='<node package="app"/>') as run:
            result = inspect_ui("target", "app", 7)
        self.assertEqual(result["serial"], "target")
        self.assertEqual(run.call_args.kwargs["timeout"], 7)
        self.assertEqual(run.call_args.args[0][-1], "target")
        self.assertEqual(run.call_args.kwargs["stderr"], subprocess.PIPE)

    def test_adb_timeout_and_serial_are_preserved(self):
        with patch("android_inspect.subprocess.check_output", return_value="value") as run:
            self.assertEqual(adb("-s", "target", "shell", "getprop", "ro.serialno"), "value")
        self.assertEqual(run.call_args.args[0][0:3], ["adb", "-s", "target"])
        self.assertEqual(run.call_args.kwargs["timeout"], 20)

    def test_password_masking_inherits_to_descendants(self):
        result = compact_ui('<node package="app" password="true"><node package="app" hint="secret"/></node>', "app")
        self.assertEqual(result["nodes"][1]["hint"], "[REDACTED]")

    def test_invalid_deadlines_are_rejected(self):
        for value in ("0", "-1", "301", "nan", "inf"):
            with self.assertRaises(Exception):
                positive_timeout(value)

    def test_empty_input_hint_is_retained(self):
        result = compact_ui('<node package="app" text="" hint="Search"/>', "app")
        self.assertEqual(result["nodes"][0]["hint"], "Search")


if __name__ == "__main__":
    unittest.main()
