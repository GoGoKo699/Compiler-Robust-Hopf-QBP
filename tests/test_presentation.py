"""Dependency-free guards for protected math and measured layout failures."""
from __future__ import annotations

import unittest
from pathlib import Path

from scripts.check_presentation import (
    ESCAPED_PUNCTUATION, geometry_failures, math_tokens, prose_lines,
)

ROOT = Path(__file__).resolve().parents[1]


class PresentationTests(unittest.TestCase):
    def test_protected_math_is_not_a_software_code_span(self) -> None:
        source = r'Call `regular_coordinate_mask(atol=...)`; use $`O\!\left(n+N/(n+m)\right)`$ and $a_j$.'
        tokens = math_tokens(source)
        self.assertEqual([t['body'] for t in tokens], [r'O\!\left(n+N/(n+m)\right)', 'a_j'])
        self.assertEqual([t['protected'] for t in tokens], [True, False])

    def test_markdown_sensitive_prose_math_is_protected(self) -> None:
        failures = []
        count = 0
        for path in ROOT.rglob('*.md'):
            if any(p.startswith('.') or p in {'node_modules', '__pycache__'} for p in path.relative_to(ROOT).parts):
                continue
            for number, line in prose_lines(path.read_text(encoding='utf-8')):
                for token in math_tokens(line):
                    if ESCAPED_PUNCTUATION.search(token['body']):
                        count += 1
                        if not token['protected']:
                            failures.append(f'{path.relative_to(ROOT)}:{number}: {token["source"]}')
        self.assertGreater(count, 0)
        self.assertEqual(failures, [])

    def test_fences_and_approved_tables_are_outside_the_prose_check(self) -> None:
        sample = 'Prose $a_j$.\n```math\nO\\!\\left(N\\right)\n```\n| $O\\!\\left(N\\right)$ | table |\nEnd $m$.\n'
        self.assertEqual([n for n, _ in prose_lines(sample)], [1, 6])

    def test_measured_overflow_is_a_failure(self) -> None:
        data = {'width': 500, 'height': 100, 'texts': [
            {'x': 25, 'y': 25, 'w': 260, 'h': 20, 'text': 'too wide'}],
            'rects': [{'x': 10, 'y': 10, 'w': 200, 'h': 60, 'id': 'box'}]}
        self.assertTrue(any('padding' in s for s in geometry_failures(data)))
        data['texts'][0]['w'] = 160
        self.assertEqual(geometry_failures(data), [])

    def test_measured_label_and_panel_overlaps_are_failures(self) -> None:
        data = {'width': 500, 'height': 500, 'texts': [
            {'x': 30, 'y': 30, 'w': 100, 'h': 24, 'text': 'marker'},
            {'x': 40, 'y': 45, 'w': 100, 'h': 24, 'text': 'response'}], 'rects': []}
        self.assertTrue(any('overlapping labels' in s for s in geometry_failures(data)))
        data['texts'] = []
        data['rects'] = [
            {'x': 10, 'y': 10, 'w': 100, 'h': 80, 'id': 'a', 'disjoint': True},
            {'x': 80, 'y': 40, 'w': 100, 'h': 80, 'id': 'b', 'disjoint': True}]
        self.assertTrue(any('overlapping panels' in s for s in geometry_failures(data)))

    def test_connector_crossing_and_hidden_arrowhead_are_failures(self) -> None:
        data = {'width': 500, 'height': 300, 'texts': [
            {'x': 30, 'y': 30, 'w': 100, 'h': 24, 'text': 'one UCG', 'clear': True}],
            'rects': [], 'edges': [{'points': [[50, 0], [50, 40], [50, 100]]}]}
        self.assertTrue(any('connector crosses' in s for s in geometry_failures(data)))
        data['texts'] = []
        data['rects'] = [{'x': 200, 'y': 80, 'w': 250, 'h': 150, 'id': 'result'}]
        data['arrows'] = [{'target': 'result', 'tip': [230, 130]}]
        self.assertTrue(any('arrowhead' in s for s in geometry_failures(data)))
        data['arrows'][0]['tip'] = [200, 130]
        self.assertEqual(geometry_failures(data), [])


if __name__ == '__main__':
    unittest.main()
