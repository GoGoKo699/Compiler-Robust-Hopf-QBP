"""Browser-level SVG layout and Markdown-to-MathJax regression checks.

Optional tooling only: numerical validation does not depend on a browser.
The Markdown handoff models GitHub's documented protected inline syntax; it
is not an authenticated screenshot of GitHub's private rendering pipeline.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = {
    "state-vs-frame.svg": 900,
    "two-qubit-obstruction.svg": 920,
    "strict-zero-echo.svg": 1020,
    "tree-cut-routing.svg": 1040,
    "literature-lineage.svg": 940,
}
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")
# Protected mathematics must be recognized before ordinary code spans.
TOKENS = re.compile(
    r"(?P<protected>\$`(?P<protected_body>[^`\n]+)`\$)"
    r"|(?P<code>(?<!`)(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`))"
    r"|(?P<plain>(?<![\\$])\$(?![$`])(?P<plain_body>[^$\n]+?)(?<!\\)\$(?!\$))"
)
ESCAPED_PUNCTUATION = re.compile(r"\\[!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~]")


def math_tokens(line: str) -> list[dict[str, Any]]:
    """Return mathematical spans without treating software code as math."""
    return [
        {"start": m.start(), "end": m.end(), "source": m.group(),
         "body": m.group("protected_body") or m.group("plain_body"),
         "protected": m.group("protected") is not None}
        for m in TOKENS.finditer(line) if m.group("code") is None
    ]


def prose_lines(text: str):
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
        if fence is None and not line.lstrip().startswith("|"):
            yield number, line


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def visible_text(markup: str) -> str:
    parser = _Text()
    parser.feed(markup)
    return "".join(parser.parts)


def markdown_handoff(source: str, renderer: Any) -> str:
    """Preserve protected TeX through CommonMark, then hand it to MathJax."""
    markup = renderer.renderInline(source)
    return re.sub(r"\$<code>(.*?)</code>\$", lambda m: "$" + m[1] + "$", markup)


def contains(rect: dict, x: float, y: float) -> bool:
    return rect["x"] <= x <= rect["x"] + rect["w"] and rect["y"] <= y <= rect["y"] + rect["h"]


def overlap(a: dict, b: dict) -> bool:
    return (min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]) > 0.5
            and min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]) > 0.5)


def geometry_failures(data: dict) -> list[str]:
    """Check native-unit geometry, independent of the CSS display scale."""
    errors: list[str] = []
    texts, rects = data["texts"], data["rects"]
    canvas = {"x": 0, "y": 0, "w": data["width"], "h": data["height"]}
    for i, text in enumerate(texts):
        cx, cy = text["x"] + text["w"] / 2, text["y"] + text["h"] / 2
        containers = [r for r in rects if contains(r, cx, cy)] or [canvas]
        parent = min(containers, key=lambda r: r["w"] * r["h"])
        pad = min(text["x"] - parent["x"], text["y"] - parent["y"],
                  parent["x"] + parent["w"] - text["x"] - text["w"],
                  parent["y"] + parent["h"] - text["y"] - text["h"])
        if pad < 6 - 0.5:
            errors.append(f"text padding {pad:.1f}px: {text['text']}")
        if not (contains(canvas, text["x"], text["y"])
                and contains(canvas, text["x"] + text["w"], text["y"] + text["h"])):
            errors.append(f"text outside SVG canvas: {text['text']}")
        for other in texts[i + 1:]:
            if overlap(text, other):
                errors.append(f"overlapping labels: {text['text']} / {other['text']}")
        if text.get("clear"):
            safe = {"x": text["x"] - 3, "y": text["y"] - 3,
                    "w": text["w"] + 6, "h": text["h"] + 6}
            for edge in data.get("edges", []):
                if any(contains(safe, *pt) for pt in edge["points"]):
                    errors.append(f"connector crosses label: {text['text']}")
                    break
    panels = [r for r in rects if r.get("disjoint")]
    for i, a in enumerate(panels):
        for b in panels[i + 1:]:
            if overlap(a, b):
                errors.append(f"overlapping panels: {a['id']} / {b['id']}")
    for arrow in data.get("arrows", []):
        target = next(r for r in rects if r["id"] == arrow["target"])
        x, y = arrow["tip"]
        # These two annotated arrows enter the left side of the result box.
        if not (target["x"] - 12 <= x <= target["x"] + 0.5
                and target["y"] + 8 <= y <= target["y"] + target["h"] - 8):
            errors.append(f"hidden or detached arrowhead: {arrow['target']}")
    return errors


MEASURE = r"""() => {
 const svg = document.querySelector('svg'), vb = svg.viewBox.baseVal;
 const root = svg.getBoundingClientRect(), scale = root.width / vb.width;
 const bbox = e => { const r = e.getBoundingClientRect(); return {
   x:(r.x-root.x)/scale, y:(r.y-root.y)/scale, w:r.width/scale, h:r.height/scale,
   id:e.id || '', text:e.textContent.trim()
 }; };
 const local = (e,p) => {const q=new DOMPoint(p.x,p.y).matrixTransform(e.getScreenCTM());
   return [(q.x-root.x)/scale,(q.y-root.y)/scale];};
 const shapes = Array.from(svg.querySelectorAll('line,path')).filter(e=>!e.closest('defs'));
 const edges = shapes.map(e=>{const length=e.getTotalLength(), count=Math.max(1,Math.ceil(length/2));
   return {points:Array.from({length:count+1},(_,i)=>local(e,e.getPointAtLength(length*i/count)))};});
 const arrows = Array.from(svg.querySelectorAll('[data-arrow-target]')).map(e=>{
   const len=e.getTotalLength(), a=e.getPointAtLength(Math.max(0,len-1)),b=e.getPointAtLength(len);
   const norm=Math.hypot(b.x-a.x,b.y-a.y), extra=3;
   return {target:e.dataset.arrowTarget,tip:local(e,{x:b.x+extra*(b.x-a.x)/norm,y:b.y+extra*(b.y-a.y)/norm})};
 });
 return {width:vb.width,height:vb.height,
   texts:Array.from(svg.querySelectorAll('text')).map(e=>({...bbox(e),clear:e.dataset.clearConnectors==='true'})),
   rects:Array.from(svg.querySelectorAll('rect')).map(e=>({...bbox(e),disjoint:e.dataset.disjointPanel==='true'})),
   edges,arrows};
}"""


def check_math(page: Any, root: Path, mathjax: Path, output: Path) -> dict:
    from markdown_it import MarkdownIt
    renderer = MarkdownIt("commonmark", {"html": True})
    expressions: dict[str, dict] = {}
    protected_count = 0
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") or part in {"node_modules", "__pycache__"} for part in path.relative_to(root).parts):
            continue
        for number, line in prose_lines(path.read_text(encoding="utf-8")):
            for token in math_tokens(line):
                converted = markdown_handoff(token["source"], renderer)
                expected = "$" + token["body"] + "$"
                if visible_text(converted) != expected:
                    raise AssertionError(f"Markdown changed TeX in {path}:{number}: {token['source']}")
                if ESCAPED_PUNCTUATION.search(token["body"]) and not token["protected"]:
                    raise AssertionError(f"unprotected Markdown-sensitive TeX in {path}:{number}")
                protected_count += token["protected"]
                expressions.setdefault(token["body"], {"markup": converted,
                    "location": f"{path.relative_to(root)}:{number}"})
    if not expressions:
        raise AssertionError("No repository prose mathematics found.")
    entries = list(expressions.items())
    body = "".join(f'<p data-math-index="{i}"><small>{html.escape(item[1]["location"])}</small> '
                   + item[1]["markup"] + '</p>' for i, item in enumerate(entries))
    page.set_content('<style>body{font:18px Arial,sans-serif;margin:24px;line-height:1.7}'
                     'p{padding:8px;border-bottom:1px solid #ddd}small{display:block;font-size:12px}</style>' + body)
    page.evaluate("window.MathJax={startup:{typeset:false},tex:{inlineMath:[['$','$']]},svg:{fontCache:'local'}}")
    page.add_script_tag(content=mathjax.read_text(encoding="utf-8"))
    page.evaluate("() => MathJax.startup.promise.then(() => MathJax.typesetPromise())")
    error_nodes = page.locator('[data-mml-node="merror"],mjx-merror,.MathJax_Error')
    if error_nodes.count():
        raise AssertionError(f"MathJax errors: {error_nodes.all_text_contents()}")
    count = page.locator('mjx-container').count()
    if count != len(entries):
        raise AssertionError(f"MathJax rendered {count} of {len(entries)} unique expressions")
    # A Markdown-consumed negative-space command must not become factorial.
    indices = [i for i, (tex, _) in enumerate(entries) if r"\!" in tex and "!" not in tex.replace(r"\!", "")]
    for i in indices:
        if page.locator(f'p[data-math-index="{i}"] [data-c="21"]').count():
            raise AssertionError(f"Spacing command became literal ! in {entries[i][0]}")
    # Preserve an inspectable typeset DOM, not a dependency on a remote script.
    rendered = page.evaluate("() => {const d=document.documentElement.cloneNode(true);d.querySelectorAll('script').forEach(x=>x.remove());return '<!doctype html>'+d.outerHTML}")
    (output / 'inline-math-rendered.html').write_text(rendered, encoding='utf-8')
    page.set_viewport_size({"width": 980, "height": 600})
    page.screenshot(path=str(output / 'inline-math-desktop.png'))
    page.set_viewport_size({"width": 390, "height": 700})
    page.screenshot(path=str(output / 'inline-math-narrow.png'))
    return {"unique_expressions": count, "protected_occurrences": protected_count,
            "spacing_command_cases": len(indices), "tex_errors": 0,
            "pipeline": "CommonMark, documented protected-token handoff, MathJax SVG; not GitHub's private filter"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--browser', help='Optional Chromium executable path')
    parser.add_argument('--mathjax', type=Path, help='Local MathJax tex-svg-full.js bundle')
    parser.add_argument('--svg-only', action='store_true')
    args = parser.parse_args()
    if not args.svg_only and (args.mathjax is None or not args.mathjax.is_file()):
        parser.error('Supply --mathjax /path/to/tex-svg-full.js, or use --svg-only.')
    from playwright.sync_api import sync_playwright
    args.output.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {"diagrams": {}, "failures": []}
    with sync_playwright() as pw:
        options: dict[str, Any] = {"headless": True}
        if args.browser:
            options['executable_path'] = args.browser
        browser = pw.chromium.launch(**options)
        page = browser.new_page(device_scale_factor=1)
        # Everything is supplied locally. Rendering must not transmit content.
        page.route('**/*', lambda route: route.abort())
        for name, desktop_width in WIDTHS.items():
            svg = (args.root / 'assets' / name).read_text(encoding='utf-8')
            report['diagrams'][name] = {}
            for mode, width in [('desktop', desktop_width), ('narrow', 358)]:
                page.set_viewport_size({"width": width + 32, "height": 900})
                page.set_content(f'<style>body{{margin:16px}}svg{{display:block;width:{width}px;height:auto}}</style>'+svg)
                page.evaluate('document.fonts.ready')
                data = page.evaluate(MEASURE)
                failures = geometry_failures(data)
                report['diagrams'][name][mode] = {'width': width, 'failures': failures,
                    'text_elements': len(data['texts'])}
                report['failures'].extend(f'{name}/{mode}: {e}' for e in failures)
                page.locator('svg').screenshot(path=str(args.output / f'{Path(name).stem}-{mode}.png'))
                if mode == 'desktop':
                    (args.output / f'{Path(name).stem}-geometry.json').write_text(json.dumps(data, indent=2), encoding='utf-8')
        if not args.svg_only:
            report['inline_math'] = check_math(page, args.root, args.mathjax, args.output)
        browser.close()
    (args.output / 'presentation-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    if report['failures']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
