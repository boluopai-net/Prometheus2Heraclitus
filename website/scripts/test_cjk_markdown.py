"""Regression for visible bold markers at Chinese punctuation boundaries."""
import unittest

import markdown
from cjk_markdown import CjkBoldExtension


class CjkBoldTests(unittest.TestCase):
    def test_adjacent_chinese_and_punctuation(self):
        rendered = markdown.markdown('前**UI**与**中文：**内容', extensions=[CjkBoldExtension()])
        self.assertEqual(rendered, '<p>前<strong>UI</strong>与<strong>中文：</strong>内容</p>')

    def test_inline_boundaries_remain_intact(self):
        rendered = markdown.markdown(
            r'`**代码**` \*\*原样\*\* **[链接](https://example.com)：**内容',
            extensions=[CjkBoldExtension()])
        self.assertEqual(rendered, '<p><code>**代码**</code> **原样** '
                         '<strong><a href="https://example.com">链接</a>：</strong>内容</p>')


if __name__ == '__main__':
    unittest.main()
