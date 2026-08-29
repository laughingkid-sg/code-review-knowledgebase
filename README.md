# Code Review Knowledgebase

Markdown rule repository for the intelligent code review demo.

This repository stores reusable review knowledge only. PRD and TD summaries are generated during a pull request run in the implementation repository and uploaded as CI artifacts; they are not stored here.

Knowledgebase rules focus on coding errors, coding mistakes, maintainability risks, security risks, and engineering practices. PRD/TD alignment is handled by the separate business-rules pipeline.

## Layers

Rules are organized by scope and language. Each layer/language keeps rules in one `RULES.md` file:

```text
common/
  go/
    RULES.md
demo/
  go/
    RULES.md
  demo-project/
    go/
      RULES.md
docs/
```

- `common/go`: company-wide Go rules.
- `demo/go`: department-level Go rules for the demo department.
- `demo/demo-project/go`: project-level Go rules for `code-review-demo`.

Target repositories decide which layers to load in their `.code-review.yml`.

## Loading Strategy

The agent should read one `RULES.md` file per configured layer. For `code-review-demo`, that means three reads:

1. `common/go/RULES.md`
2. `demo/go/RULES.md`
3. `demo/demo-project/go/RULES.md`

This avoids reading hundreds of small files during CI while preserving common, department, and project-level rule layering.

## Rule IDs

Use stable rule IDs so findings can be tracked, disabled, counted, and improved over time.

Suggested prefixes:

- `GO-COM-###`: common Go rules.
- `GO-DEMO-###`: demo department Go rules.
- `GO-DEMO-PROJ-###`: demo project Go rules.

## Rule Format

Rules use pure markdown without YAML front matter. Each rule starts with a level-two linked heading for navigation, followed by a small metadata table and standard sections.

The scope and language are derived from the `RULES.md` path, so they are not repeated in every rule table. The agent keeps the full rule for reporting and governance, but sends a compact rule payload to the LLM that excludes `Contributor`, `Tags`, and `References`.

```markdown
## [Always close HTTP response bodies](#close-http-response-bodies)

| Field | Value |
| --- | --- |
| ID | `GO-COM-001` |
| Slug | `close-http-response-bodies` |
| Contributor | `example@gmail.com` |
| Severity | `P2` |
| Tags | `resource-management` |
| References | None |

### Rule

Describe the rule.

### Background

Explain the context behind the rule.

### Risks

Explain correctness, performance, security, or maintainability risks.

### Review Checklist

Describe what the reviewer should inspect.

### Good Example

```go
defer resp.Body.Close()
```

### Bad Example

```go
resp, _ := http.Get(url)
_ = resp
```

### Review Comment Guidance

Explain how the finding should be written to the developer.
```

## Disabled Rules

Rules can be disabled by ID in a target repository config when a broader rule intentionally does not apply to that repo. The agent should skip rule sections whose metadata table has a disabled `ID`.

## Contributor Field

- `Contributor`: email that originally contributed the rule or most recent substantial update.

## Severity

Severity represents both impact and review priority for this demo:

- `P0`: critical security, data loss, outage, or severe production risk.
- `P1`: likely correctness, reliability, or security issue.
- `P2`: maintainability, observability, performance, or moderate correctness risk.
- `P3`: readability, consistency, or minor improvement.
