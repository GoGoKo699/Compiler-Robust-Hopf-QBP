#!/usr/bin/env python3
"""Check whether the recorded upstream branch heads have moved."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "provenance" / "upstream.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Validate and display provenance without network access.",
    )
    return parser.parse_args()


def load_provenance() -> dict[str, object]:
    with PROVENANCE.open("r", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schema_version") != 2:
        raise ValueError("Unsupported provenance schema version.")
    upstreams = payload.get("tracked_upstreams")
    if not isinstance(upstreams, list) or not upstreams:
        raise ValueError("No tracked upstream repositories are recorded.")
    for record in upstreams:
        if not isinstance(record, dict):
            raise ValueError("Every tracked upstream must be an object.")
        repository = record.get("repository")
        branch = record.get("branch")
        commit = record.get("commit")
        if not isinstance(repository, str) or "/" not in repository:
            raise ValueError("Invalid upstream repository name.")
        if not isinstance(branch, str) or not branch:
            raise ValueError("Invalid upstream branch name.")
        if not isinstance(commit, str) or len(commit) != 40:
            raise ValueError("Invalid upstream commit SHA.")
        try:
            int(commit, 16)
        except ValueError as exc:
            raise ValueError("Invalid upstream commit SHA.") from exc
    return payload


def github_branch_sha(repository: str, branch: str) -> str:
    url = f"https://api.github.com/repos/{repository}/commits/{branch}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "compiler-robust-hopf-sync-audit",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    sha = payload.get("sha")
    if not isinstance(sha, str) or len(sha) != 40:
        raise ValueError(
            f"GitHub returned no valid commit SHA for {repository}:{branch}."
        )
    return sha


def main() -> int:
    args = parse_args()
    try:
        payload = load_provenance()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    records = payload["tracked_upstreams"]
    assert isinstance(records, list)
    if args.offline:
        for record in records:
            assert isinstance(record, dict)
            print(
                f"recorded {record['repository']}:{record['branch']} "
                f"at {record['commit']}"
            )
        return 0

    stale = False
    for record in records:
        assert isinstance(record, dict)
        repository = str(record["repository"])
        branch = str(record["branch"])
        expected = str(record["commit"])
        try:
            current = github_branch_sha(repository, branch)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"error checking {repository}:{branch}: {exc}", file=sys.stderr)
            return 2
        marker = "OK" if current == expected else "DRIFT"
        print(f"{marker} {repository}:{branch} recorded={expected} current={current}")
        stale |= current != expected
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
