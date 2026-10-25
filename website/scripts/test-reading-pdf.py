"""Regression for CJK emphasis lost by GFM's delimiter-flanking rules."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('reading_pdf', Path(__file__).with_name('build-reading-pdf.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReaderRegression(unittest.TestCase):
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
