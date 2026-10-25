"""Regression for concept names diverging between website and PDF readers."""
import unittest
from reader_names import reader_names, reader_document, reader_text


class ReaderNames(unittest.TestCase):
    def test_html_and_pdf_share_labels_without_changing_destinations(self):
        source = '阴阳与太极、双鱼和无极'
        expected = 'Yinyang与Taiji、Shuang yu和Wuji'
        href = '/阴阳/#太极'
        self.assertEqual(reader_names(f'<a href="{href}">{source}</a>'),
                         f'<a href="{href}">{expected}</a>')
        link = {'t': 'Link', 'c': [['', [], []], [{'t': 'Str', 'c': source}], [href, '']]}
        result = reader_document(link)
        self.assertEqual(result['c'][1][0]['c'], expected)
        self.assertEqual(result['c'][2][0], href)

    def test_quotes_code_and_ordinary_words_remain_source_material(self):
        quotation = '「阴阳之义配日月」'
        self.assertEqual(reader_text(quotation), quotation)
        self.assertEqual(reader_text('「阴阳」与' + quotation), '「Yinyang」与' + quotation)
        self.assertEqual(reader_text('《太极图说》与太极图说'), '《太极图说》与太极图说')
        source = '<blockquote>阴阳之义配日月</blockquote><code>阴阳</code>'
        self.assertEqual(reader_names(source), source)
        code = {'t': 'Code', 'c': [['', [], []], '阴阳']}
        self.assertEqual(reader_document(code), code)
        self.assertEqual(reader_text('阳光、阴影、物理主义与自然主义'),
                         '阳光、阴影、物理主义与自然主义')


if __name__ == '__main__':
    unittest.main()
