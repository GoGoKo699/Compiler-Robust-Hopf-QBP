"""One-time, base-pinned presentation patch preparation; not retained."""
from pathlib import Path
import hashlib
import json
import re
import runpy
import subprocess
import tempfile
import xml.etree.ElementTree as ET

PIN = '7f47e5917d0874f06f90aed2143784c054fbf0f8'
ROOT = Path('assets')
BASE = Path(tempfile.mkdtemp(prefix='hopf-asset-baseline-'))
(BASE / 'assets').mkdir()

def git(*args):
    return subprocess.check_output(['git', *args])

def blob_sha(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

assert git('rev-parse', 'origin/main').decode().strip() == PIN
ASSET_BASE = {
    'state-vs-frame.svg': '6b7318a96d5e1e4fb0f016e122f8d88f52925f30',
    'two-qubit-obstruction.svg': '71559ba738afe88be1a69186c1e4bfc992b90691',
    'strict-zero-echo.svg': '5ee9d4e47437cc0f03cfeedad8bc84d7cebc4816',
    'tree-cut-routing.svg': '08614565a19fab0b92b39d7f1c03958ae4715b0e',
    'literature-lineage.svg': 'c57be71ffdf18621044f3a00a38697d8d4b4cae0',
}
for name, expected in ASSET_BASE.items():
    raw=git('show',f'{PIN}:assets/{name}')
    assert blob_sha(raw)==expected
    (BASE/'assets'/name).write_bytes(raw)

p=ROOT/'state-vs-frame.svg';s=(BASE/'assets'/p.name).read_text()
s=s.replace('translate(105,190)','translate(75,190)').replace('translate(735,190)','translate(705,190)')
s=s.replace('width="360" height="190"','width="420" height="190"')
s=s.replace('x="104" y="18" width="70"','x="104" y="18" width="88"')
s=s.replace('x="190" y="18" width="70"','x="208" y="18" width="88"')
s=s.replace('x="276" y="18" width="66"','x="312" y="18" width="90"')
for old,new in [(139,148),(225,252),(309,357),(180,210)]:
    s=s.replace(f'<text x="{old}"',f'<text x="{new}"')
p.write_text(s)

p=ROOT/'two-qubit-obstruction.svg';s=(BASE/'assets'/p.name).read_text()
s=s.replace('height="540"','height="575"').replace('viewBox="0 0 1200 540"','viewBox="0 0 1200 575"')
s=s.replace('height="310"','height="338"').replace('y="367"','y="392"')
s=s.replace('y="425" width="870"','y="456" width="870"').replace('y="458"','y="489"').replace('y="490"','y="521"')
p.write_text(s)

p=ROOT/'strict-zero-echo.svg';s=(BASE/'assets'/p.name).read_text()
for i,x in enumerate([545,1075],1):
    s=s.replace(f'<text x="{x}" y="300" text-anchor="middle" class="small">one UCG</text>',
    f'<text id="ucg-note-{i}" data-clear-connectors="true" x="{x+61}" y="288" text-anchor="start" class="small">one UCG</text>')
p.write_text(s)

p=ROOT/'tree-cut-routing.svg';s=(BASE/'assets'/p.name).read_text()
s=s.replace('<text x="250" y="310" text-anchor="middle" class="label">cut after t depths</text>',
    '<text id="cut-label" data-clear-connectors="true" x="250" y="307" text-anchor="middle" class="label"><tspan x="250">cut after</tspan><tspan x="250" dy="27">t depths</tspan></text>')
s=s.replace('M220,249 C190,315 180,345 180,390','M220,249 C165,294 180,340 198,390')
s=s.replace('M280,249 C310,315 320,345 320,390','M280,249 C335,294 320,340 338,390')
s=s.replace('width="590" height="475"','width="590" height="490"')
s=s.replace('y1="356" x2="295" y2="394"','y1="356" x2="295" y2="388"')
s=s.replace('<rect x="75" y="406" width="440" height="50"', '<rect id="inverse-router-box" x="55" y="400" width="480" height="76"')
s=s.replace('<text x="295" y="438" text-anchor="middle" class="body">inverse router restores the suffix and returns every work register to |0⟩</text>',
    '<text id="inverse-router-caption" x="295" y="430" text-anchor="middle" class="body"><tspan x="295">inverse router restores the suffix</tspan><tspan x="295" dy="25">and returns every work register to |0⟩</tspan></text>')
p.write_text(s)

p=ROOT/'literature-lineage.svg';s=(BASE/'assets'/p.name).read_text()
s=s.replace('height="600"','height="640"').replace('viewBox="0 0 1400 600"','viewBox="0 0 1400 640"')
# Move lane headings above their respective box rows.
s=s.replace('x="55" y="132"','id="state-preparation-lane" x="55" y="96"')
s=s.replace('x="55" y="362"','id="hopf-lane" x="55" y="357"')
# Reflow each row, retaining every text string and all typography.
for row,old_y,new_y in [('upper',88,115),('lower',318,376)]:
    for i,(old_x,new_x,old_w,new_w,old_c,new_c) in enumerate([
        (205,55,235,275,323,192.5),(528,385,235,275,646,522.5),(851,715,270,285,986,857.5)]):
        s=s.replace(f'<rect x="{old_x}" y="{old_y}" width="{old_w}" height="96"',
            f'<rect id="{row}-stage-{i+1}" data-disjoint-panel="true" x="{new_x}" y="{new_y}" width="{new_w}" height="112"')
        for off in [34,60,83]:
            s=s.replace(f'<text x="{old_c}" y="{old_y+off}"', f'<text x="{new_c}" y="{new_y+off+4}"')
    for old_a,old_b,new_a,new_b in [(440,516,330,373),(763,839,660,703)]:
        s=s.replace(f'<line x1="{old_a}" y1="{old_y+48}" x2="{old_b}" y2="{old_y+48}"',
            f'<line x1="{new_a}" y1="{new_y+56}" x2="{new_b}" y2="{new_y+56}"')
s=s.replace('M986,184 C1010,245 1100,245 1135,285','M1000,171 H1045 V287 H1087')
s=s.replace('M1121,366 C1160,366 1160,305 1135,285','M1000,432 H1045 V341 H1087')
s=s.replace('<rect x="1065" y="228" width="285" height="130"',
    '<rect id="compiler-result" data-disjoint-panel="true" x="1090" y="244" width="275" height="140"')
for old,new in [(267,278),(296,307),(322,359-26),(346,359)]:
    s=s.replace(f'<text x="1208" y="{old}"', f'<text x="1227.5" y="{new}"')
s=s.replace('x="185" y="492" width="1030" height="72"','x="90" y="530" width="1220" height="82"')
s=s.replace('x="700" y="521"','x="700" y="561"').replace('x="700" y="548"','x="700" y="589"')
p.write_text(s)

p=ROOT/'state-vs-frame.svg'
s=p.read_text().replace('y="97" text-anchor="middle" class="small"','y="92" text-anchor="middle" class="small"').replace('y="119" text-anchor="middle" class="small"','y="123" text-anchor="middle" class="small"')
p.write_text(s)
p=ROOT/'tree-cut-routing.svg'
s=p.read_text().replace('>cut after</tspan>','>cut after </tspan>').replace('>inverse router restores the suffix</tspan>','>inverse router restores the suffix </tspan>')
p.write_text(s)
p=ROOT/'literature-lineage.svg'
s=p.read_text().replace('<path d="M1000,171','<path data-arrow-target="compiler-result" d="M1000,171').replace('<path d="M1000,432','<path data-arrow-target="compiler-result" d="M1000,432')
p.write_text(s)

ASSET_FINAL = {'literature-lineage.svg': '9ea411f45a8f36513d9f54d1993a2188774e17b9', 'state-vs-frame.svg': 'a7c1c9ff4374799994b61ee76ecce95236c4065f', 'strict-zero-echo.svg': '1d5d0f88a6a318abd1de681323afcd304065cdf7', 'tree-cut-routing.svg': '424a15dfbe096e0b694643882d80e37305cf000f', 'two-qubit-obstruction.svg': '164149d8ebc5475b92a8c65fcb3f26ea2de9c7b3'}
for name, expected in ASSET_FINAL.items():
    raw=(ROOT/name).read_bytes()
    assert blob_sha(raw)==expected, (name,blob_sha(raw),expected)
    # Layout edits must retain every label and the complete original palette.
    old=ET.fromstring((BASE/'assets'/name).read_bytes())
    new=ET.fromstring(raw)
    ns={'s':'http://www.w3.org/2000/svg'}
    texts=lambda tree: [' '.join(''.join(e.itertext()).split()) for e in tree.findall('.//s:text',ns)]
    assert texts(old)==texts(new),name
    assert old.find('.//s:style',ns).text==new.find('.//s:style',ns).text,name

# Install the small persistent checker; discard all preparation machinery later.
for source,dest in {
    '_presentation_browser.py':'scripts/check_presentation.py',
    '_presentation_unit_tests.py':'tests/test_presentation.py',
    '_presentation_requirements.txt':'requirements-presentation.txt',
    '_presentation_ci.yml':'.github/workflows/presentation.yml',
}.items():
    Path(dest).write_bytes(Path(source).read_bytes())
    Path(source).unlink()

api=runpy.run_path('scripts/check_presentation.py')
from markdown_it import MarkdownIt
md=MarkdownIt('commonmark',{'html':True})
paths=git('ls-tree','-r','--name-only',PIN).decode().splitlines()
changed={}
for relative in paths:
    if not relative.endswith('.md'):
        continue
    p=Path(relative)
    old=git('show',f'{PIN}:{relative}').decode('utf-8')
    lines=old.splitlines(keepends=True)
    hits=0
    for number,line in api['prose_lines'](old):
        tokens=api['math_tokens'](line)
        result=lines[number-1]
        for token in reversed(tokens):
            if token['protected']:
                continue
            rendered=api['markdown_handoff'](token['source'],md)
            risk=(api['ESCAPED_PUNCTUATION'].search(token['body']) or
                  api['visible_text'](rendered)!='$'+token['body']+'$')
            if risk:
                result=result[:token['start']]+'$`'+token['body']+'`$'+result[token['end']:]
                hits+=1
        assert [t['body'] for t in tokens]==[t['body'] for t in api['math_tokens'](result)]
        lines[number-1]=result
    new=''.join(lines)
    # Every edited character is a protective backtick; the underlying TeX,
    # approved tables and all fenced display/code blocks are unchanged.
    unprotect=lambda text: re.sub(r'\$`([^`\n]+)`\$',lambda m:'$'+m[1]+'$',text)
    assert unprotect(new)==unprotect(old),relative
    if hits:
        p.write_text(new,encoding='utf-8')
        changed[relative]=hits

p=Path('tests/test_math_typography.py')
s=p.read_text()
anchor='KNOWN_CODE = {'
assert s.count(anchor)==1
s=s.replace(anchor, 'PROTECTED_MATH = re.compile(r"\\$`([^`\\n]+)`\\$")\n'+anchor)
old='for match in INLINE_CODE.finditer(line):'
assert s.count(old)==1
s=s.replace(old,'for match in INLINE_CODE.finditer(PROTECTED_MATH.sub("", line)):')
old='without_code = INLINE_CODE.sub("", line)'
assert s.count(old)==1
s=s.replace(old, 'without_code = INLINE_CODE.sub("", PROTECTED_MATH.sub(lambda m: "$" + m[1] + "$", line))')
old='for body in INLINE_MATH.findall(line):'
assert s.count(old)==1
s=s.replace(old,'for body in INLINE_MATH.findall(PROTECTED_MATH.sub(lambda m: "$" + m[1] + "$", line)):')
p.write_text(s)

# Keep optional rendering instructions beside the diagram map, not in the proof.
p=Path('assets/README.md')
p.write_text(p.read_text()+r"""
## Rendering checks

The optional [presentation checker](../scripts/check_presentation.py) renders
all five SVGs at their desktop embedding widths and at a 358-pixel image width.
It measures label containment, label overlap, annotated connector clearance and
visible arrowheads. It also checks that prose mathematics survives a CommonMark
handoff and typesets with MathJax. This models the documented protected inline
syntax; it does not reproduce GitHub's private client implementation.

The numerical compiler suite remains independent of these browser dependencies.

```bash
python -m pip install -r requirements-presentation.txt
python -m playwright install chromium
npm install --prefix /tmp/hopf-mathjax --ignore-scripts --no-audit --no-fund mathjax-full@3.2.1
python scripts/check_presentation.py \
  --mathjax /tmp/hopf-mathjax/node_modules/mathjax-full/es5/tex-svg-full.js \
  --output /tmp/hopf-presentation
```

Use `--svg-only` to inspect the diagrams without the optional MathJax bundle.
The browser checker emits previews and measured geometry for inspection.
""")

# The exact clean tree, not the temporary preparation branch, is validated.
Path('.github/workflows/prepare-presentation.yml').unlink()
Path(__file__).unlink()
allowed=set(changed)|{f'assets/{x}' for x in ASSET_FINAL}|{
    'assets/README.md','scripts/check_presentation.py','tests/test_presentation.py',
    'tests/test_math_typography.py','requirements-presentation.txt',
    '.github/workflows/presentation.yml'}
subprocess.run(['git','add','-A'],check=True)
actual=set(git('diff','--cached','--name-only',PIN).decode().splitlines())
assert actual<=allowed,actual-allowed
for name in paths:
    if name.startswith('compiler_robust_hopf/') and name.endswith('.py'):
        assert Path(name).read_bytes()==git('show',f'{PIN}:{name}'),name
    if name.startswith('.github/workflows/'):
        assert Path(name).read_bytes()==git('show',f'{PIN}:{name}'),name
print(json.dumps({'protected_math_by_page':changed,'total_protected':sum(changed.values()),
                  'changed_files':sorted(actual),'asset_hashes':ASSET_FINAL,
                  'approved_tables_and_fences':'unchanged','scientific_python':'unchanged'},indent=2))
