"""Dependency-free guards for protected math and measured layout failures."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts.check_presentation import (
    ESCAPED_PUNCTUATION, geometry_failures, math_tokens, prose_lines,
    native_equation_is_stacked, native_math_failures,
)

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_MATH = re.compile(r"\$`[^`\n]+`\$")
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(`+)(.+?)\1")
NATIVE_UNSUPPORTED_NUMBERING = re.compile(
    r"\\tag\*?(?![A-Za-z])"
    r"|\\begin\s*\{(?:equation|align|alignat|gather|multline|flalign)\}"
)


def unsupported_math_numbering(text: str) -> list[tuple[int, str]]:
    """Find math commands that produce unsupported native labeled rows.

    Scan math fences and prose, including dollar displays and protected inline
    math. Literal commands inside ordinary code spans or other fences are not
    mathematical input and must remain usable in explanations and examples.
    """
    failures = []
    fence = None
    math_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
                math_fence = line[marker.end():].strip() == 'math'
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
                math_fence = False
            continue
        if fence is not None:
            bodies = [line] if math_fence else []
        else:
            bodies = [match.group() for match in PROTECTED_MATH.finditer(line)]
            bodies.append(CODE_SPAN.sub('', PROTECTED_MATH.sub('', line)))
        for body in bodies:
            failures.extend((number, match.group())
                            for match in NATIVE_UNSUPPORTED_NUMBERING.finditer(body))
    return failures


def raw_less_than_in_math(text: str) -> list[tuple[int, str]]:
    """Find HTML-sensitive less-than characters only in mathematical input."""
    failures = []
    fence = None
    math_fence = False
    dollar_display = False
    for number, line in enumerate(text.splitlines(), 1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
                math_fence = line[marker.end():].strip() == 'math'
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
                math_fence = False
            continue
        if fence is not None:
            bodies = [line] if math_fence else []
        else:
            bodies = [token['body'] for token in math_tokens(line)]
            # Ignore dollar-display markers quoted in literal code examples.
            remaining = CODE_SPAN.sub('', PROTECTED_MATH.sub('', line))
            pieces = remaining.split('$$')
            for index, piece in enumerate(pieces):
                if dollar_display:
                    bodies.append(piece)
                if index + 1 < len(pieces):
                    dollar_display = not dollar_display
        failures.extend((number, body) for body in bodies if '<' in body)
    return failures


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
    def test_html_sensitive_comparisons_are_detected_in_math(self) -> None:
        source = (
            '```math\n\\begin{cases}a,&j<m-1\\\\b,&j=m-1\\end{cases}\n```\n'
            '```math\n\\sum_{d<r}2^d\n```\n'
            'Use $`j<m`$ and $a<b$.\n'
            '$$\nx<y\n$$\n'
        )
        self.assertEqual([line for line, _ in raw_less_than_in_math(source)],
                         [2, 5, 7, 7, 9])

    def test_html_and_code_examples_are_not_mathematical_comparisons(self) -> None:
        source = (
            '<img src="figure.svg" width="400">\n'
            '<details><summary>Proof</summary></details>\n'
            'Literal `x<y` and `$$x<y$$` are code examples.\n'
            '```python\nassert x < y\n```\n'
            'Use $`j\\lt m`$ and $a\\lt b$.\n'
            '```math\n\\sum_{d\\lt r}2^d\n```\n'
        )
        self.assertEqual(raw_less_than_in_math(source), [])

    def test_repository_math_uses_html_safe_comparisons(self) -> None:
        failures = []
        for path in ROOT.rglob('*.md'):
            if any(p.startswith('.') or p in {'node_modules', '__pycache__'}
                   for p in path.relative_to(ROOT).parts):
                continue
            failures.extend(f'{path.relative_to(ROOT)}:{number}: {expression}'
                            for number, expression in raw_less_than_in_math(
                                path.read_text(encoding='utf-8')))
        self.assertEqual(failures, [])

    def test_native_unsupported_numbering_is_detected_in_mathematical_input(self) -> None:
        source = (
            '```math\na=b\\tag{1}\n```\n'
            '$$c=d\\tag*{A}$$\n'
            '$`x=y\\tag{2}`$\n'
            '```math\n\\begin{equation}\nx=y\n\\end{equation}\n```\n'
        )
        self.assertEqual(unsupported_math_numbering(source), [
            (2, r'\tag'), (4, r'\tag*'), (5, r'\tag'),
            (7, r'\begin{equation}'),
        ])
        for environment in ('align', 'alignat', 'gather', 'multline', 'flalign'):
            with self.subTest(environment=environment):
                self.assertTrue(unsupported_math_numbering(
                    '```math\n\\begin{' + environment + '}\nx=y\n```\n'))

    def test_native_numbering_guard_preserves_supported_math_and_code_examples(self) -> None:
        source = (
            'The literal `\\tag{1}` is an example.\n'
            '```latex\n\\begin{equation}\na=b\\tag{1}\n```\n'
            '```math\na=b\\qquad\\text{(1)}\n'
            '\\begin{aligned}x&=y\\\\z&=w\\end{aligned}\n'
            '\\begin{cases}0,&x<0\\\\1,&x>0\\end{cases}\n'
            '\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}\n```\n'
        )
        self.assertEqual(unsupported_math_numbering(source), [])

    def test_repository_math_avoids_native_unsupported_numbering(self) -> None:
        failures = []
        for path in ROOT.rglob('*.md'):
            if any(p.startswith('.') or p in {'node_modules', '__pycache__'}
                   for p in path.relative_to(ROOT).parts):
                continue
            failures.extend(f'{path.relative_to(ROOT)}:{number}: {command}'
                            for number, command in unsupported_math_numbering(
                                path.read_text(encoding='utf-8')))
        self.assertEqual(failures, [])

    def test_native_geometry_detects_stacking_without_rejecting_multiline_math(self) -> None:
        # The short theorem condition occupied a narrow column 132px tall in
        # the live failure, despite having neither a fraction nor multiple rows.
        broken = dict(ink_width=20, ink_height=132, font_size=16,
                      token_count=13, rows=0)
        self.assertTrue(native_equation_is_stacked(broken))
        horizontal = dict(broken, ink_width=280, ink_height=24)
        self.assertFalse(native_equation_is_stacked(horizontal))
        # Genuine matrices and cases may be tall and narrow. Their multiple
        # ordinary rows distinguish them from glyphs stacked in one math row.
        self.assertFalse(native_equation_is_stacked(dict(broken, rows=3)))
        self.assertFalse(native_equation_is_stacked(dict(broken, token_count=5)))
        self.assertFalse(native_equation_is_stacked(dict(broken, fractions=2)))
        self.assertFalse(native_equation_is_stacked(dict(broken, roots=1)))

    def test_native_labeled_rows_and_measured_stacking_are_failures(self) -> None:
        valid = {'unsupported_numbered_rows': 0, 'equations': []}
        self.assertEqual(native_math_failures(valid), [])
        self.assertTrue(native_math_failures(dict(valid, unsupported_numbered_rows=1)))
        self.assertTrue(native_math_failures(dict(valid, equations=[
            {'index': 1, 'ink_width': 20, 'ink_height': 132, 'font_size': 16,
             'token_count': 13, 'rows': 0},
        ])))

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
