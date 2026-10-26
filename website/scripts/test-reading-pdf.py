"""Focused regressions for the reading edition's source-to-book conversion."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('reading_pdf', Path(__file__).with_name('build-reading-pdf.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReaderRegression(unittest.TestCase):
    def test_practical_guides_are_collected_without_duplicate_web_navigation(self):
        for english in (False, True):
            suffix = '.md' if english else '.zh-CN.md'
            sections = builder.book_paths(english)
            self.assertEqual(sections[-1][1], [builder.PACKAGE + 'references/docs/' + name + suffix
                             for name in ('getting-started', 'research-and-learning', 'psychological-support')])
        source = '# Psychology\n\n## Page navigation\n\n<nav class="guide-navigation" markdown="1">\n- [Materials](#materials)\n</nav>\n\n## Materials\n\nUseful explanation.'
        result = builder.prepare_markdown(source)
        self.assertNotIn('Page navigation', result)
        self.assertNotIn('<nav', result)
        self.assertIn('## Materials\n\nUseful explanation.', result)

    def test_navigation_is_removed_when_language_link_is_not_first(self):
        for navigation in (
            '[阴阳说明](../../README.zh-CN.md) · [实践说明](creation-method.zh-CN.md) · [English](participation-and-support.md)',
            '[YinYang guide](../../README.md) · [Practice explanation](creation-method.md) · [完整中文版](participation-and-support.zh-CN.md)',
            '[中文版](philosophical-readings.zh-CN.md) · [Psychological readings](psychological-readings.md)',
        ):
            with self.subTest(navigation=navigation):
                prose = 'Read the [English](source.md) argument in context.'
                result = builder.prepare_markdown('# Chapter\n\n' + navigation + '\n\n' + prose)
                self.assertNotIn(navigation, result)
                self.assertIn(prose, result)
                self.assertEqual(builder.prepare_markdown('[A primary source](source.md)'), '[A primary source](source.md)')

    def test_core_views_follows_the_whole_main_sequence(self):
        for english in (False, True):
            suffix = '.md' if english else '.zh-CN.md'
            paths = [p for _, members in builder.book_paths(english) for p in members]
            mainline = [builder.PACKAGE + 'references/docs/' + name + suffix
                        for _, _, essays in builder.GROUPS for name, _ in essays]
            core = builder.PACKAGE + 'references/docs/core-views' + suffix
            self.assertGreater(paths.index(core), max(paths.index(p) for p in mainline))
            self.assertEqual(len(paths), len(set(paths)))

    def test_cjk_emphasis_with_parenthetical_and_adjacent_text(self):
        source = '这叫**凝缩（Verdichtung）**，同时**充实言说（parole pleine，亦译「充分言说」）**有用。'
        doc = builder.parse(source)
        emphasized = []

        def collect(node):
            if node.get('t') == 'Strong':
                emphasized.append(builder.plain(node['c']))
            return node

        builder.walk(doc, collect)
        self.assertEqual(emphasized, ['凝缩（Verdichtung）', '充实言说（parole pleine，亦译「充分言说」）'])
        self.assertNotIn('**', builder.plain(doc['blocks']))


if __name__ == '__main__':
    unittest.main()
