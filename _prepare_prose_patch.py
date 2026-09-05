from __future__ import annotations

import collections
import json
import re
import string
import subprocess
from pathlib import Path

BASE = "714111972f9aa257cd2f5e4f54976bd368d6f93e"
ROOT = Path.cwd()

# Each nontrivial conversion is enumerated, not inferred from exponent syntax.
REPLACEMENTS = {letter: letter for letter in string.ascii_letters}
IDENTITIES = """
(b,y)
(B-1)(s+1)-t
(B-1)s
(b_s,y_s)
(h,b)
(N-1)
-2
0,1,2,3
2
2^j(s+1)
2^j(s+1)-1
2^jw-1
2^n-1
2^t
2B(s+1)
2N-1
3B-2-t
4n
[z=0]
A_d
a_j
B-1
B-1-t
b=0
b=1
B=2^t
B_d
br
C_p
C_p X C_p X
d+1
d+2
d<n-1
d=0
d=n-1
d=n-2
D_O
F_t
h(r)=1
h=1
J
L_0
L_d
m-1
m=0
n+m
n+m<5n
n,m
n,t
N-1
n-d-2
n=1
N=2^n
n=8
n^2
p,r
P_0
P_d
R_t
s+1
s=1
s=n-t
s=n-t>1
s>1
S_E
t=n-1
T_h
T_h=X_b
X,C_p,X,C_p
x=zb
"""
REPLACEMENTS.update({s: s for s in IDENTITIES.splitlines() if s})
PAIRS = r"""
(ell,u) => (\ell,u)
-2 Y_ancilla tensor K_(d,r) => -2Y_{\mathrm{ancilla}}\otimes K_{d,r}
0,...,d => 0,\ldots,d
0,...,n-2 => 0,\ldots,n-2
1/2 => \frac12
1/4 => \frac14
11t-4=O(t) => 11t-4=O(t)
1<=m<4n => 1\leq m<4n
2**d => 2^d
2**n-1 => 2^n-1
2**n/(n+m) => \frac{2^n}{n+m}
2^s/s=O(N/(n+m)) => \frac{2^s}{s}=O\!\left(\frac{N}{n+m}\right)
[0,2pi) => [0,2\pi)
[0,pi/2] => [0,\pi/2]
A_d|0^n> => A_d\lvert0^n\rangle
a_j(theta) => a_j(\boldsymbol\theta)
a_j=sqrt(g_(j,j)) => a_j=\sqrt{g_{j,j}}
a_j>=0 => a_j\geq0
b xor h => b\oplus h
B2^s=2^n => B2^s=2^n
B2^s=N => B2^s=N
B_tilde_d => \widetilde B_d
B_tilde_d^dagger => \widetilde B_d^{\dagger}
beta_0 => \beta_0
beta_1 => \beta_1
C**(-1) => C^{-1}
C**2=U => C^2=U
C^2=R_y(theta) => C^2=R_y(\theta)
C_bad => C_{\mathrm{bad}}
chi => \chi
cos(pi/2) => \cos(\pi/2)
D=Omega(2**n/(n+m)) => D=\Omega\!\left(\frac{2^n}{n+m}\right)
D=Omega(n) => D=\Omega(n)
D_frame => D_{\mathrm{frame}}
D_frame(n,m) => D_{\mathrm{frame}}(n,m)
D_ph => D_{\mathrm{ph}}
D_prep(n,m) => D_{\mathrm{prep}}(n,m)
delta => \delta
epsilon_infinity => \varepsilon_\infty
F_t^(n) => F_t^{(n)}
G=Omega(2**n) => G=\Omega(2^n)
g_(j,j)=0 => g_{j,j}=0
g_(j,j)=a_j^2 => g_{j,j}=a_j^2
g_(j,j)>0 => g_{j,j}>0
j=0,...,t-1 => j=0,\ldots,t-1
K_(d,r) => K_{d,r}
L_d^(n) => L_d^{(n)}
lambda(j) => \lambda(j)
M=Theta(2**n) => M=\Theta(2^n)
M=Theta(2^n) => M=\Theta(2^n)
M=Theta(N) => M=\Theta(N)
m>=0 => m\geq0
m>=1 => m\geq1
m>=2^{n+1}=2N => m\geq2^{n+1}=2N
m>=2N => m\geq2N
m>=4n => m\geq4n
n**3=O(2**n) => n^3=O(2^n)
N/(n+m) => N/(n+m)
N/(n+m)=O(1) => N/(n+m)=O(1)
N=2**n => N=2^n
n=Theta(log M) => n=\Theta(\log M)
n>=1 => n\geq1
n^2=O(2^n/n) => n^2=O(2^n/n)
n^2=O(N/n) => n^2=O(N/n)
n^3=O(2^n) => n^3=O(2^n)
O(2**d) => O(2^d)
O(2**n) => O(2^n)
O(2**q) => O(2^q)
O(2^d) => O(2^d)
O(2^n) => O(2^n)
O(2^n/n) => O(2^n/n)
O(2^s) => O(2^s)
O(2^t) => O(2^t)
O(B(s+1)) => O(B(s+1))
O(B) => O(B)
O(B+s) => O(B+s)
O(D(n+m)) => O(D(n+m))
O(G) => O(G)
O(log n)=O(log log M) => O(\log n)=O(\log\log M)
O(N log n) => O(N\log n)
O(N) => O(N)
O(n) => O(n)
O(n+2**n/(n+m)) => O\!\left(n+\frac{2^n}{n+m}\right)
O(n+2^n/n) => O(n+2^n/n)
O(n+N/(n+m)) => O\!\left(n+\frac{N}{n+m}\right)
O(n+N/n) => O(n+N/n)
O(n-d) => O(n-d)
O(n2^D) => O(n2^D)
O(n^2) => O(n^2)
O(nD) => O(nD)
O(q+2**q/(q+w)) => O\!\left(q+\frac{2^q}{q+w}\right)
O(s^2+2^s/s) => O(s^2+2^s/s)
O(t) => O(t)
Omega(2**n/n) => \Omega(2^n/n)
Omega(2^n) => \Omega(2^n)
Omega(N) => \Omega(N)
Omega(n) => \Omega(n)
Omega(N/(n+m)) => \Omega\!\left(\frac{N}{n+m}\right)
Omega(N/n) => \Omega(N/n)
phi_l => \phi_\ell
pi/4 => \pi/4
Q_perp P=P => Q_\perp P=P
Q|00>=|00> => Q\lvert00\rangle=\lvert00\rangle
R_t^(n) => R_t^{(n)}
R_y(theta_p) => R_y(\theta_p)
S=O(log n) => S=O(\log n)
s>=2 => s\geq2
S_grad => S_\nabla
sqrt(g_(j,j)) => \sqrt{g_{j,j}}
sqrt(g_(j,j))=|a_j| => \sqrt{g_{j,j}}=\lvert a_j\rvert
SU(2) => \mathrm{SU}(2)
t>=1 => t\geq1
Theta(2**n) => \Theta(2^n)
Theta(N) => \Theta(N)
Theta(n) => \Theta(n)
Theta(n+2**n/(n+m)) => \Theta\!\left(n+\frac{2^n}{n+m}\right)
Theta(n+2**n/n) => \Theta(n+2^n/n)
Theta(n+N/n) => \Theta(n+N/n)
U(2) => \mathrm{U}(2)
U_tilde => \widetilde U
V_tilde => \widetilde V
V|0>=W|0> => V\lvert0\rangle=W\lvert0\rangle
W^dagger => W^{\dagger}
W_(C,mag) => W_{\mathbb C,\mathrm{mag}}
W_(C,mag)=D_ph W_R => W_{\mathbb C,\mathrm{mag}}=D_{\mathrm{ph}}W_{\mathbb R}
W_R => W_{\mathbb R}
W_R(theta) => W_{\mathbb R}(\boldsymbol\theta)
W_R^dagger => W_{\mathbb R}^{\dagger}
W_tilde => \widetilde W
W_tilde J = J W => \widetilde WJ=JW
W_tilde J_m=J_m W => \widetilde WJ_m=J_mW
W_tilde^dagger => \widetilde W^{\dagger}
W|0^n> => W\lvert0^n\rangle
XCX=C^(-1) => XCX=C^{-1}
X|+>=|+> => X\lvert+\rangle=\lvert+\rangle
|00> => \lvert00\rangle
|01> => \lvert01\rangle
|0> => \lvert0\rangle
|0>|e_x>|0> => \lvert0\rangle\lvert e_x\rangle\lvert0\rangle
|0^m> => \lvert0^m\rangle
|0^n> => \lvert0^n\rangle
|0^s> => \lvert0^s\rangle
|10> => \lvert10\rangle
|11> => \lvert11\rangle
|a_j| => \lvert a_j\rvert
|alpha> => \lvert\alpha\rangle
|e_j> => \lvert e_j\rangle
|varphi> => \lvert\varphi\rangle
|x>|0> => \lvert x\rangle\lvert0\rangle
|xi_r> => \lvert\xi_r\rangle
|z|=n-d-1 => \lvert z\rvert=n-d-1
"""
for entry in PAIRS.strip().splitlines():
    source, sep, replacement = entry.partition(" => ")
    assert sep and source and replacement
    REPLACEMENTS[source] = replacement

INLINE_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
FENCE = re.compile(r"^(?:\s*>\s*)*\s*(`{3,}|~{3,})")


def rows(text):
    fence = None
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = FENCE.match(line)
        protected = fence is not None or marker is not None
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        yield number, line, protected, line.lstrip().startswith("|") and not protected


def protected_content(text):
    return [line for _, line, fenced, table in rows(text) if fenced or table]


def git(*args):
    return subprocess.check_output(["git", *args], text=True)


def replace_once(text, before, after):
    assert text.count(before) == 1, repr(before)
    return text.replace(before, after, 1)


QUANTIFIERS = (
    "The upper bounds hold for every parameter tuple. The matching lower bounds\n"
    "hold in the worst case over the Hopf-frame family, uniformly in the\n"
    "clean-workspace budget. They do not impose the same cost on every individual\n"
    "frame.\n\n"
)


def main():
    assert git("rev-parse", "origin/main").strip() == BASE, "main moved; rebase explicitly"
    paths = git("ls-tree", "-r", "--name-only", BASE).splitlines()
    converted = collections.Counter()
    remaining = collections.defaultdict(list)
    changed = []
    for relative in paths:
        if not relative.endswith(".md"):
            continue
        before = git("show", f"{BASE}:{relative}")
        output = []
        for number, line, fenced, table in rows(before):
            if fenced or table:
                output.append(line)
                continue
            def convert(match):
                value = match.group(2)
                if value not in REPLACEMENTS:
                    remaining[value].append(f"{relative}:{number}")
                    return match.group(0)
                converted[value] += 1
                return "$" + REPLACEMENTS[value] + "$"
            output.append(INLINE_CODE.sub(convert, line))
        after = "".join(output)
        if relative == "README.md":
            after = replace_once(after, "The real result concerns the complete Hopf differential frame.",
                                 QUANTIFIERS + "The real result concerns the complete Hopf differential frame.")
        elif relative == "REVIEW.md":
            after = replace_once(after, "The complex unitary is the phase-dressed magnitude frame",
                                 QUANTIFIERS + "The complex unitary is the phase-dressed magnitude frame")
        elif relative == "docs/COMPILER_THEOREM.md":
            after = replace_once(after, "The proof is assembled from the three schedules below",
                                 QUANTIFIERS + "The proof is assembled from the three schedules below")
            after = replace_once(after,
                "implements $L_d^{(n)}$ exactly and restores every system qubit.",
                "implements $L_d^{(n)}$ exactly, with the borrowed suffix bit restored\n"
                "and no additional sector-dependent phase.")
        assert protected_content(before) == protected_content(after), relative
        if before != after:
            (ROOT / relative).write_text(after, encoding="utf-8")
            changed.append(relative)

    # Existing checks still enforce the same statement, now in math rather than code.
    relative = "tests/test_clean_room_review.py"
    text = git("show", f"{BASE}:{relative}")
    text = replace_once(text, 'self.assertIn("for every integer `m>=0`", text)',
                        'self.assertIn(r"for every integer $m\\geq0$", text)')
    text = replace_once(text, 'self.assertIn("If `s=1`", text)',
                        'self.assertIn("If $s=1$", text)')
    (ROOT / relative).write_text(text, encoding="utf-8")
    relative = "tests/test_reviewer_narrative.py"
    text = git("show", f"{BASE}:{relative}")
    text = replace_once(text, 'self.assertIn("If `s=1`", theorem)',
                        'self.assertIn("If $s=1$", theorem)')
    (ROOT / relative).write_text(text, encoding="utf-8")

    # This test module is supplied with the preparation script on its temporary branch.
    test_source = ROOT / "_math_typography_test.py"
    (ROOT / "tests/test_math_typography.py").write_text(test_source.read_text(), encoding="utf-8")

    # Restore the entire baseline index; stage only the intended patch files.
    git("read-tree", BASE)
    intended = changed + ["tests/test_clean_room_review.py", "tests/test_reviewer_narrative.py",
                          "tests/test_math_typography.py"]
    git("add", "--", *intended)
    assert set(git("diff", "--cached", "--name-only", BASE).splitlines()) == set(intended)
    for relative in paths:
        if relative.endswith(".py") and relative not in intended:
            assert (ROOT / relative).read_text(encoding="utf-8") == git("show", f"{BASE}:{relative}"), relative

    print("APPROVED TABLES AND ALL FENCED BLOCKS: BYTE-IDENTICAL")
    print("SCIENTIFIC PYTHON IMPLEMENTATION AND EXISTING WORKFLOWS: UNCHANGED")
    print(json.dumps({"modified_markdown_files": len(changed), "converted_occurrences": sum(converted.values()),
                      "unique_conversions": len(converted), "changed_files": intended}, indent=2))
    print("\nREVIEWED CONVERSION MAP")
    for value in sorted(converted):
        print(f"{converted[value]:3d} {value!r} -> {REPLACEMENTS[value]!r}")
    print("\nPRESERVED CODE SPANS (outside tables and fences)")
    for value, locations in sorted(remaining.items()):
        print(f"{value!r}: {', '.join(locations)}")

    # Keep temporary files out of tests' filesystem traversal and the exported tree.
    test_source.unlink()
    Path(__file__).unlink()
    (ROOT / ".github/workflows/prepare-prose-cleanup.yml").unlink()


if __name__ == "__main__":
    main()
