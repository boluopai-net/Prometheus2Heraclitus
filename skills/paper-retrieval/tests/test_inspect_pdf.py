import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_pdf.py"
spec = importlib.util.spec_from_file_location("inspect_pdf", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def make_pdf():
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>",
               b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    stream = b"BT /F1 12 Tf 20 100 Td (Disposable test paper) Tj ET"
    objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    data = b"%PDF-1.4\n"
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += str(number).encode() + b" 0 obj\n" + obj + b"\nendobj\n"
    xref = len(data)
    data += b"xref\n0 6\n0000000000 65535 f \n"
    data += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    data += f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return data


class InspectionTests(unittest.TestCase):
    def test_rejects_error_page_and_broken_pdf(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "error.pdf"
            path.write_text("<html>Access denied</html>")
            with self.assertRaises(ValueError):
                helper.inspect(path)
            if shutil.which("pdfinfo") and shutil.which("pdftotext"):
                path.write_bytes(b"%PDF-broken")
                with self.assertRaises(subprocess.CalledProcessError):
                    helper.inspect(path)

    @unittest.skipUnless(shutil.which("pdfinfo") and shutil.which("pdftotext"), "Poppler unavailable")
    def test_real_cli_reports_bytes_and_text_without_identity_claim(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "paper.pdf"
            path.write_bytes(make_pdf())
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    check=True, capture_output=True, text=True)
            report = json.loads(result.stdout)
            self.assertEqual(report["pages"], 1)
            self.assertEqual(report["bytes"], path.stat().st_size)
            self.assertEqual(len(report["sha256"]), 64)
            self.assertIn("Disposable test paper", report["samples"]["first_page"])
            self.assertFalse(report["identity_verified"])
            self.assertFalse(report["completeness_verified"])


if __name__ == "__main__":
    unittest.main()
