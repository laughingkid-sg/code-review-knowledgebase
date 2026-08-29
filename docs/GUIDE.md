# Knowledgebase Guide

## Purpose

This repository stores markdown review rules for the code review agent. It does not store generated PRD or TD summaries.

Rules in this repository should focus on code quality, correctness, security, maintainability, and common implementation mistakes. Business requirement alignment against PRD/TD documents belongs to the separate business-rules pipeline.

## Current Demo Layers

The `code-review-demo` repository loads these layers:

1. `common/go/RULES.md`
2. `demo/go/RULES.md`
3. `demo/demo-project/go/RULES.md`

## Adding Rules

Add new rules to the relevant layer/language `RULES.md` file. Keep rule IDs stable because future metrics will use them to track findings, upvotes, downvotes, consumption, and non-consumption.

Each rule should use this shape:

```markdown
## [Short rule title](#short-rule-slug)

| Field | Value |
| --- | --- |
| ID | `GO-COM-001` |
| Slug | `short-rule-slug` |
| Contributor | `example@gmail.com` |
| Severity | `P2` |
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

## Contributor

Use `Contributor` for the email that supplied the rule content. This supports future review routing and rule effectiveness reporting.

## Severity

Use `Severity` for both impact and review priority:

- `P0`: critical security, data loss, outage, or severe production risk.
- `P1`: likely correctness, reliability, or security issue.
- `P2`: maintainability, observability, performance, or moderate correctness risk.
- `P3`: readability, consistency, or minor improvement.
