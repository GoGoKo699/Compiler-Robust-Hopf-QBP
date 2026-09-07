"""One-time preparation helper; excluded from the published patch tree."""
from pathlib import Path
from copy import deepcopy
import json
import os
import subprocess

BASE = 'e2bc1e7d3959453b478e36888617b398966e6f8e'
EXPECTED_TREE = '6985dbb658f0a4c01b20e80d617885deb153e23a'
FINAL_BRANCH = 'upstream-reconciliation-20260907'
ROOT = Path(os.environ['RUNNER_TEMP']) / 'hopf-reconciliation-clean'
OLD = 'faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582'
NEW = 'a9885317cf998a7df87ca07ba86e3bd4f0f419ef'


def run(*args, cwd=ROOT):
    subprocess.run(args, cwd=cwd, check=True)


run('git', 'worktree', 'add', '--detach', str(ROOT), BASE, cwd=Path.cwd())


def replace(rel, before, after, expected=1):
    path = ROOT / rel
    text = path.read_text(encoding='utf-8')
    assert text.count(before) == expected, (rel, before, text.count(before))
    path.write_text(text.replace(before, after), encoding='utf-8')


path = ROOT / 'provenance/upstream.json'
payload = json.loads(path.read_text())
original = deepcopy(payload)
payload['recorded_at_utc'] = '2026-09-07T11:33:27Z'
main = next(r for r in payload['upstreams'] if r['repository'] == 'GoGoKo699/Hopf-QBP' and r['tracked_branch'] == 'main')
assert main['tracked_commit'] == OLD
main['tracked_commit'] = NEW
previous = deepcopy(payload['upstream_reconciliation'])
payload['upstream_reconciliation'] = {
    'previous_main_commit': OLD,
    'reviewed_main_commit': NEW,
    'commits_reviewed': 5,
    'reviewed_at_utc': payload['recorded_at_utc'],
    'changed_upstream_paths': [
        'docs/CLAIM_SUPPORT.md',
        'docs/OBSERVABLES_AND_READOUT.md',
        'docs/STATISTICAL_ACCURACY.md',
        'qbp_validation/tests/test_documentation.py',
        'validate_qbp.py',
    ],
    'relevant_changes': [
        'raw coordinatewise l_infinity remains the primary finite-shot target; normalized-frame and natural-gradient outputs retain their separate conditioning',
        'the ambient-sphere phase metric is the adopted convention; the projective metric remains a comparison only',
        'reflection-sum sampling is stated with coefficient-one-norm scaling and a matched controlled-observable comparator',
        'zero-weight magnitude records vanish; zero-amplitude phase derivatives have zero mean records, but individual phase records need not vanish',
        'the upstream claim map is repaired and documentation-integrity checks are added; circuit builders, decoders, and the headline sampling theorem are unchanged',
    ],
    'local_resolution': 'Reviewed the five-commit upstream diff. Existing output-task, metric, and controlled-observable boundaries remain applicable. Scoped the zero-record statements in docs/QBP_CONSEQUENCE.md and SYNC.md explicitly to magnitude coordinates. Updated current-baseline references and provenance tests. Preserved the previous reconciliation, original file lineage, historical seed, and frozen fallback; no scientific implementation or approved layout was changed.'
}
payload['upstream_reconciliation_history'] = [previous]
assert payload['file_lineage'] == original['file_lineage']
assert payload['frozen_fallback'] == original['frozen_fallback']
assert payload['upstreams'][1:] == original['upstreams'][1:]
path.write_text(json.dumps(payload, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

replace('SYNC.md', f'  `{OLD}`;', f'  `{NEW}`;')
replace('SYNC.md', 'and the current baseline', 'and the baseline adopted at that time')
replace('SYNC.md',
        '3. a zero metric weight makes the raw differential and raw estimator vanish,\n   while inverse-metric outputs become ill-conditioned near small weights;',
        '3. a zero magnitude metric weight makes the raw magnitude differential and\n   estimator vanish, while inverse-metric outputs become ill-conditioned near\n   small weights;')
new_note = '''## Reconciliation completed on 2026-09-07

The five commits from the September 3 baseline

```text
faddc98da5c1fdd07ce42df2b04ca7b6ce3e2582
```

to the newly tracked baseline

```text
a9885317cf998a7df87ca07ba86e3bd4f0f419ef
```

were reviewed in full. The changes synchronize manuscript terminology for
raw-coordinate and geometric outputs, the ambient-sphere phase metric, and
reflection-sum sampling with matched controlled-observable costs. They also
repair the upstream claim map and add documentation-integrity tests. No circuit
builder, decoder, or headline sampling theorem changes in this interval.

One clarification is relevant locally: zero-weight magnitude records vanish,
whereas zero-amplitude phase derivatives have zero mean records but need not
have zero individual signed one-hot records. The zero-record statement in the
QBP consequence and the zero-weight statement above now explicitly concern
magnitude coordinates. The existing frame, sampling, and cost arguments are
unchanged.

The current-baseline references and provenance tests are updated together. The
September 3 reconciliation is retained in
`upstream_reconciliation_history`, and original file lineage, the historical
seed, and the frozen fallback remain unchanged. No upstream implementation was
copied and no approved layout was altered.

'''
replace('SYNC.md', '## Synchronization procedure\n', new_note+'## Synchronization procedure\n')
replace('SYNC.md', 'The audit never modifies either repository automatically.',
        'The online audit also runs when the provenance record or audit machinery\nchanges, before and after merge, as well as on its existing schedule and manual\ntrigger. Ordinary numerical validation remains offline. The audit never\nmodifies either repository automatically.')
replace('docs/QBP_CONSEQUENCE.md',
        'At a singular coordinate, the raw coordinate record is exactly zero.',
        'At a singular magnitude coordinate, the raw coordinate record is exactly zero.')
for rel in ['docs/SOURCE_MAP.md', 'docs/PROOF_AUDIT.md', 'tests/test_reviewer_narrative.py']:
    replace(rel, OLD, NEW)
replace('tests/test_provenance.py', f'CURRENT_HOPF_QBP_MAIN = "{OLD}"',
        f'PREVIOUS_HOPF_QBP_MAIN = "{OLD}"\nCURRENT_HOPF_QBP_MAIN = "{NEW}"')
replace('tests/test_provenance.py',
        '        self.assertEqual(reconciliation["commits_reviewed"], 10)',
        '        self.assertEqual(reconciliation["previous_main_commit"], PREVIOUS_HOPF_QBP_MAIN)\n        self.assertEqual(reconciliation["commits_reviewed"], 5)')
new_tests = '''    def test_previous_reconciliation_and_file_lineage_are_retained(self) -> None:
        history = self.payload["upstream_reconciliation_history"]
        self.assertTrue(history)
        previous = history[-1]
        self.assertEqual(previous["reviewed_main_commit"], PREVIOUS_HOPF_QBP_MAIN)
        self.assertEqual(previous["commits_reviewed"], 10)
        self.assertEqual(
            previous["previous_main_commit"],
            "9957815767ef3649275960fd5e860fb91725ff26",
        )
        self.assertEqual(
            previous["reviewed_main_commit"],
            self.payload["upstream_reconciliation"]["previous_main_commit"],
        )
        for sources in self.payload["file_lineage"].values():
            self.assertTrue(all(CURRENT_HOPF_QBP_MAIN not in source for source in sources))
        seed = next(
            record for record in self.payload["upstreams"]
            if record["tracked_branch"] == "ancilla-depth-robustness-2026"
        )
        self.assertEqual(seed["tracked_commit"], "9cc564f493caff62b847fc362df522a68c6e83bf")

    def test_current_baseline_references_match_the_provenance(self) -> None:
        for relative in ("docs/SOURCE_MAP.md", "docs/PROOF_AUDIT.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(CURRENT_HOPF_QBP_MAIN, text, relative)
            self.assertNotIn(PREVIOUS_HOPF_QBP_MAIN, text, relative)

    def test_zero_record_clarification_is_magnitude_specific(self) -> None:
        qbp = " ".join((ROOT / "docs/QBP_CONSEQUENCE.md").read_text(encoding="utf-8").split())
        sync = " ".join((ROOT / "SYNC.md").read_text(encoding="utf-8").split())
        self.assertIn(
            "At a singular magnitude coordinate, the raw coordinate record is exactly zero.",
            qbp,
        )
        self.assertNotIn("At a singular coordinate, the raw coordinate record is exactly zero.", qbp)
        self.assertIn("a zero magnitude metric weight", sync)
        self.assertIn("need not have zero individual signed one-hot records", sync)
        joined = " ".join(self.payload["upstream_reconciliation"]["relevant_changes"])
        self.assertIn("individual phase records need not vanish", joined)

'''
replace('tests/test_provenance.py',
        '    def test_sync_document_names_recorded_commits(self) -> None:\n',
        new_tests+'    def test_sync_document_names_recorded_commits(self) -> None:\n')
replace('.github/workflows/upstream-sync-audit.yml', 'on:\n', '''on:
  push:
    branches: [main]
    paths:
      - "provenance/upstream.json"
      - "scripts/check_upstream_sync.py"
      - ".github/workflows/upstream-sync-audit.yml"
  pull_request:
    paths:
      - "provenance/upstream.json"
      - "scripts/check_upstream_sync.py"
      - ".github/workflows/upstream-sync-audit.yml"
''')
replace('.github/workflows/upstream-sync-audit.yml',
        '  check-upstream-heads:\n    runs-on: ubuntu-latest',
        '''  check-upstream-heads:
    # Only trusted same-repository changes use the online provenance check.
    if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
    runs-on: ubuntu-latest''')

allowed = {
    '.github/workflows/upstream-sync-audit.yml', 'SYNC.md',
    'docs/PROOF_AUDIT.md', 'docs/QBP_CONSEQUENCE.md', 'docs/SOURCE_MAP.md',
    'provenance/upstream.json', 'tests/test_provenance.py',
    'tests/test_reviewer_narrative.py',
}
changed = set(subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines())
assert changed == allowed, changed
run('git', 'add', '--', *sorted(allowed))
run('git', 'diff', '--cached', '--check')
tree = subprocess.check_output(['git', 'write-tree'], cwd=ROOT, text=True).strip()
assert tree == EXPECTED_TREE, (tree, EXPECTED_TREE)
print('Exact locally validated tree reproduced:', tree, flush=True)

run('python', '-m', 'compileall', '-q', 'compiler_robust_hopf', 'scripts', 'tests', 'validate.py')
run('python', 'scripts/reviewer_walkthrough.py')
run('python', 'validate.py')
run('python', 'scripts/unified_resource_ledger.py', '--n', '12')
run('python', 'scripts/strict_zero_echo_ledger.py', '--n', '12')
run('python', 'scripts/check_upstream_sync.py', '--offline')
run('python', 'scripts/check_upstream_sync.py')
assert subprocess.check_output(['git', 'write-tree'], cwd=ROOT, text=True).strip() == EXPECTED_TREE
run('git', 'config', 'user.name', 'github-actions[bot]')
run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
run('git', 'commit', '-m', 'Reconcile the reviewed Hopf-QBP baseline and clarify magnitude scope')
# Create a new patch branch only; never force-update the default branch.
run('git', 'push', 'origin', f'HEAD:refs/heads/{FINAL_BRANCH}')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
print('FINAL_BRANCH=' + FINAL_BRANCH, flush=True)
print('FINAL_COMMIT=' + head, flush=True)
