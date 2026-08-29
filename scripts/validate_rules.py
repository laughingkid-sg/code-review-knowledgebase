#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


RULE_HEADING_RE = re.compile(r"^##\s+\[(?P<title>.+?)\]\(#(?P<slug>[a-z0-9][a-z0-9-]*)\)\s*$")
TABLE_ROW_RE = re.compile(r"^\|\s*(?P<field>[^|]+?)\s*\|\s*(?P<value>[^|]+?)\s*\|\s*$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ID_PATTERNS = {
    "common/go/RULES.md": re.compile(r"^GO-COM-\d{3}$"),
    "demo/go/RULES.md": re.compile(r"^GO-DEMO-\d{3}$"),
    "demo/demo-project/go/RULES.md": re.compile(r"^GO-DEMO-PROJ-\d{3}$"),
}
REQUIRED_FIELDS = ("ID", "Slug", "Contributor", "Severity", "Tags", "References")
DISALLOWED_FIELDS = {"Owner", "Level", "Scope", "Language", "Department", "Project"}
REQUIRED_SECTIONS = (
    "Rule",
    "Background",
    "Risks",
    "Review Checklist",
    "Good Example",
    "Bad Example",
    "Review Comment Guidance",
)


@dataclass(frozen=True)
class RuleBlock:
    path: Path
    start_line: int
    title: str
    heading_slug: str
    body: str


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors: list[str] = []
    rules_files = sorted(root.glob("**/RULES.md"))

    if not rules_files:
        errors.append("No RULES.md files found.")

    for path in rules_files:
        errors.extend(validate_rules_file(root, path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(rules_files)} RULES.md file(s).")
    return 0


def validate_rules_file(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    rel_path = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")

    if text.startswith("---"):
        errors.append(f"{rel_path}: YAML front matter is not allowed.")

    blocks = parse_rule_blocks(path, text)
    if not blocks:
        errors.append(f"{rel_path}: no linked rule headings found.")
        return errors

    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()
    id_pattern = ID_PATTERNS.get(rel_path)

    for block in blocks:
        metadata = parse_metadata_table(block.body)
        prefix = f"{rel_path}:{block.start_line}"

        for field in REQUIRED_FIELDS:
            if field not in metadata:
                errors.append(f"{prefix}: missing metadata field `{field}`.")

        for field in sorted(DISALLOWED_FIELDS.intersection(metadata)):
            errors.append(f"{prefix}: metadata field `{field}` is no longer allowed.")

        rule_id = metadata.get("ID", "")
        slug = metadata.get("Slug", "")
        contributor = metadata.get("Contributor", "")
        severity = metadata.get("Severity", "")

        if id_pattern and rule_id and not id_pattern.match(rule_id):
            errors.append(f"{prefix}: ID `{rule_id}` does not match path prefix for {rel_path}.")
        if rule_id in seen_ids:
            errors.append(f"{prefix}: duplicate ID `{rule_id}`.")
        seen_ids.add(rule_id)

        if slug != block.heading_slug:
            errors.append(f"{prefix}: heading slug `{block.heading_slug}` does not match metadata Slug `{slug}`.")
        if slug in seen_slugs:
            errors.append(f"{prefix}: duplicate Slug `{slug}`.")
        seen_slugs.add(slug)

        if contributor and not EMAIL_RE.match(contributor):
            errors.append(f"{prefix}: Contributor `{contributor}` must be an email address.")
        if severity and severity not in {"P0", "P1", "P2", "P3"}:
            errors.append(f"{prefix}: Severity `{severity}` must be P0, P1, P2, or P3.")

        for section in REQUIRED_SECTIONS:
            if f"### {section}" not in block.body:
                errors.append(f"{prefix}: missing section `### {section}`.")

    return errors


def parse_rule_blocks(path: Path, text: str) -> list[RuleBlock]:
    lines = text.splitlines()
    heading_indexes = [index for index, line in enumerate(lines) if line.startswith("## ")]
    blocks: list[RuleBlock] = []

    for offset, index in enumerate(heading_indexes):
        match = RULE_HEADING_RE.match(lines[index])
        if not match:
            continue
        end = heading_indexes[offset + 1] if offset + 1 < len(heading_indexes) else len(lines)
        blocks.append(
            RuleBlock(
                path=path,
                start_line=index + 1,
                title=match.group("title"),
                heading_slug=match.group("slug"),
                body="\n".join(lines[index + 1 : end]),
            )
        )
    return blocks


def parse_metadata_table(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        match = TABLE_ROW_RE.match(line.strip())
        if not match:
            continue
        field = match.group("field").strip()
        value = match.group("value").strip()
        if field in {"Field", "---"}:
            continue
        metadata[field] = value.replace("`", "").strip()
    return metadata


if __name__ == "__main__":
    raise SystemExit(main())
