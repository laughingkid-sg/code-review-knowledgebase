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
## GO-COM-001: short-rule-slug - Short rule title

| Field | Value |
| --- | --- |
| Owner | `example@gmail.com` |
| Contributor | `example@gmail.com` |
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

Use `Owner` for the accountable email. Use `Contributor` for the email that supplied the rule content. These fields support future review routing and rule effectiveness reporting. For the current demo, `Owner` and `Contributor` can be the same email.

## Level And Severity

Use `Level` for enforcement policy:

- `required`: should block or demand a fix when confidently detected.
- `recommended`: should normally be fixed, but may allow judgment.
- `advisory`: useful guidance with low enforcement pressure.

Use `Severity` for impact:

- `critical`: security, data loss, or severe production risk.
- `high`: likely correctness, security, or reliability issue.
- `medium`: maintainability, observability, or moderate correctness risk.
- `low`: minor readability or consistency issue.
