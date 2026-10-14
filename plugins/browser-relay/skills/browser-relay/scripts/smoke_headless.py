#!/usr/bin/env python3
"""Check ephemeral Playwright page ownership, reversible readback and cleanup."""
import argparse
import json


def smoke():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        result = {"carrier": "Playwright Chromium headless",
                  "ownership": "task-created context and live Page handle",
                  "fixture": "local content; no remote navigation or profile"}
        try:
            page.set_content('<title>Relay fixture</title><button id="change" '
                             'onclick="document.getElementById(\'value\').textContent=\'changed\'">'
                             'Change</button><p id="value">initial</p>')
            assert page.title() == "Relay fixture"
            assert context.pages == [page]
            assert page.locator("#value").inner_text() == "initial"
            page.locator("#change").click()
            result["readback"] = page.locator("#value").inner_text()
            assert result["readback"] == "changed"
        finally:
            try:
                page.close()
                result["page_closed"] = page.is_closed()
                assert result["page_closed"] and page not in context.pages
            finally:
                try:
                    context.close()
                finally:
                    browser.close()
        result["browser_disconnected"] = not browser.is_connected()
        assert result["browser_disconnected"]
        result["not_established"] = ["authentication", "retained shared owner", "desktop placement"]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        print(json.dumps(smoke(), indent=2))
    except ImportError:
        parser.exit(1, "Playwright missing; follow the optional README setup.\n")


if __name__ == "__main__":
    main()
