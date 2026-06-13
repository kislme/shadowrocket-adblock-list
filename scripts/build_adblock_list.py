from __future__ import annotations

import datetime as dt
import re
import urllib.request
from pathlib import Path


SOURCE_URL = "https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_ad_only.conf"
ROOT = Path(__file__).resolve().parents[1]

FULL_OUT = ROOT / "adblock_shadowrocket_full.list"
DOMAIN_OUT = ROOT / "adblock_shadowrocket_domain_only.list"

RULE_RE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6),(.+?),(Reject|REJECT)$")
DOMAIN_RULES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}


def fetch_source() -> str:
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "shadowrocket-adblock-list-builder/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def convert(source: str, domain_only: bool) -> list[str]:
    seen: set[str] = set()
    rules: list[str] = []

    for raw_line in source.splitlines():
        line = raw_line.strip()
        match = RULE_RE.match(line)
        if not match:
            continue

        rule_type, value, _policy = match.groups()
        if domain_only and rule_type not in DOMAIN_RULES:
            continue

        converted = f"{rule_type},{value}"
        if converted not in seen:
            seen.add(converted)
            rules.append(converted)

    return rules


def write_list(path: Path, rules: list[str], label: str) -> None:
    now = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    header = [
        f"# NAME: {label}",
        "# FORMAT: Shadowrocket RULE-SET list",
        f"# SOURCE: {SOURCE_URL}",
        f"# UPDATED: {now}",
        f"# TOTAL: {len(rules)}",
        "",
    ]
    path.write_text("\n".join(header + rules) + "\n", encoding="utf-8")


def main() -> None:
    source = fetch_source()
    write_list(FULL_OUT, convert(source, domain_only=False), "Johnshall AdBlock Full")
    write_list(DOMAIN_OUT, convert(source, domain_only=True), "Johnshall AdBlock Domain Only")


if __name__ == "__main__":
    main()
