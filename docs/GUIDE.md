# Knowledgebase Guide

## Purpose

This repository stores markdown review rules for the code review agent. It does not store generated PRD or TD summaries.

## Current Demo Layers

The `code-review-demo` repository loads these layers:

1. `common/go/RULES.md`
2. `demo/go/RULES.md`
3. `demo/demo-project/go/RULES.md`

## Adding Rules

Add new rules to the relevant layer/language `RULES.md` file. Keep rule IDs stable because future metrics will use them to track findings, upvotes, downvotes, consumption, and non-consumption.

Each rule should use this shape:

```markdown
## GO-COM-001: Short rule title

| Field | Value |
| --- | --- |
| Slug | `short-rule-slug` |
| Scope | `common` |
| Language | `go` |
| Owner | `platform-engineering` |
| Contributor | `codex` |
| Level | `recommended` |
| Severity | `medium` |
| Tags | `tag-one`, `tag-two` |
| References | None |

### Rule
### Background
### Risks
### Review Checklist
### Good Example
### Bad Example
### Review Comment Guidance
```

## Suppressing Rules

If a rule does not apply to a target repository, add its ID to `knowledge.disabled_rules` in that repo's `.code-review.yml`.

Suppressions should be rare and intentional. Prefer improving or narrowing the rule when it is too broad for multiple repos.

## Ownership

Use `Owner` for the accountable team or project. Use `Contributor` for the person, team, or automation that supplied the rule content. These fields support future review routing and rule effectiveness reporting.
