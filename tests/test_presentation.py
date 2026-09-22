"""Dependency-free guards for protected math and measured layout failures."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts.check_presentation import (
    ESCAPED_PUNCTUATION, geometry_failures, math_tokens, prose_lines,
)

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_MATH = re.compile(r"\$`[^`\n]+`\$")
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")


def malformed_protected_boundaries(text: str) -> list[tuple[int, str]]:
    """Find stray code delimiters touching protected math outside fences.

    Such delimiters can turn the intervening prose into code while isolated
    TeX rendering still succeeds. Tables are included in this syntax check.
    """
    failures = []
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        for match in PROTECTED_MATH.finditer(line):
            before = match.start() > 0 and line[match.start() - 1] == '`'
            after = match.end() < len(line) and line[match.end()] == '`'
            if before or after:
                failures.append((number, match.group()))
    return failures


class PresentationTests(unittest.TestCase):
    def test_stray_code_delimiters_around_protected_math_are_detected(self) -> None:
        broken = 'Use $`a=2`$` and `$`b=3`$.\n| $`L`$` | width |\n'
        self.assertEqual(
            malformed_protected_boundaries(broken),
            [(1, '$`a=2`$'), (1, '$`b=3`$'), (2, '$`L`$')],
        )
        valid = (
            'Call `compile()` with $`a=2`$ and $`b=3`$.\n'
            '```markdown\nUse $`a=2`$` and `$`b=3`$.\n```\n'
        )
        self.assertEqual(malformed_protected_boundaries(valid), [])

    def test_repository_protected_math_has_no_stray_code_delimiters(self) -> None:
        failures = []
        for path in ROOT.rglob('*.md'):
            if any(p.startswith('.') or p in {'node_modules', '__pycache__'}
                   for p in path.relative_to(ROOT).parts):
                continue
            for number, token in malformed_protected_boundaries(
                path.read_text(encoding='utf-8')
            ):
                failures.append(f'{path.relative_to(ROOT)}:{number}: {token}')
        self.assertEqual(failures, [])

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
            for number, line in prose_lines(path.read_text(encoding='utf-8'), include_tables=True):
                for token in math_tokens(line):
                    if line.lstrip().startswith('|') and re.search(r'(?<!\\)\|', token['body']):
                        failures.append(f'{path.relative_to(ROOT)}:{number}: table pipe inside mathematics')
                    if ESCAPED_PUNCTUATION.search(token['body']):
                        count += 1
                        if not token['protected']:
                            failures.append(f'{path.relative_to(ROOT)}:{number}: {token["source"]}')
        self.assertGreater(count, 0)
        self.assertEqual(failures, [])

    def test_fences_and_approved_tables_are_outside_the_prose_check(self) -> None:
        sample = 'Prose $a_j$.\n```math\nO\\!\\left(N\\right)\n```\n| $O\\!\\left(N\\right)$ | table |\nEnd $m$.\n'
        self.assertEqual([n for n, _ in prose_lines(sample)], [1, 6])
        self.assertEqual([n for n, _ in prose_lines(sample, include_tables=True)], [1, 5, 6])

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
