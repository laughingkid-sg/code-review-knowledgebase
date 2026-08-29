# Code Review Knowledgebase

Markdown rule repository for the intelligent code review demo.

This repository stores reusable review knowledge only. PRD and TD summaries are generated during a pull request run in the implementation repository and uploaded as CI artifacts; they are not stored here.

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

Rules use pure markdown without YAML front matter. Each rule starts with a level-two heading containing the stable rule ID and title, followed by a metadata table and standard sections:

```markdown
## GO-COM-001: Always close HTTP response bodies

| Field | Value |
| --- | --- |
| Slug | `close-http-response-bodies` |
| Scope | `common` |
| Language | `go` |
| Level | `recommended` |
| Severity | `medium` |
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

Rules can be disabled by ID in a target repository config when a broader rule intentionally does not apply to that repo. The agent should skip matching `## RULE-ID: Title` sections for disabled IDs.
