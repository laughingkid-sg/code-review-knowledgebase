# Demo Project Go Rules

Project-level Go rules for `code-review-demo`.

## GO-DEMO-PROJ-001: Keep demo APIs aligned with PRD and TD documents

| Field | Value |
| --- | --- |
| Slug | `align-demo-apis-with-prd-and-td` |
| Scope | `project` |
| Department | `demo` |
| Project | `demo-project` |
| Language | `go` |
| Owner | `demo-project` |
| Contributor | `codex` |
| Level | `required` |
| Severity | `high` |
| Tags | `business-logic`, `documentation` |
| References | `docs/PRD.md`, `docs/TDD.md` in the affected demo project |

### Rule

Changes to demo API behavior must remain consistent with the relevant PRD and TD documents for the affected demo project.

### Background

The central demo requirement is to compare implementation logic against product and technical requirements. PRD and TD summaries are generated during each pull request run as implementation-repo CI artifacts, then used by the business-rule reviewer for the specific PR.

### Risks

- Product risk: shipped behavior may not match the product requirement.
- Technical risk: implementation may bypass architecture or data-flow decisions in the TD.
- Review risk: code-only review may miss business logic defects that are visible only when compared against PRD and TD intent.

### Review Checklist

- Identify the affected demo project from `.code-review.yml`.
- Read the PR-specific PRD/TD summary artifact generated in the CI run.
- Compare changed handler, service, repository, and model behavior against the relevant requirements.
- Flag mismatches where the code implements different validation, state transitions, permissions, or persistence behavior from the documents.

### Good Example

```go
if req.Price <= 0 {
	return ErrInvalidPrice
}
```

### Bad Example

```go
product.Price = req.Price
```

### Review Comment Guidance

Reference the affected PRD or TD requirement in plain language, then explain the implementation mismatch and required code change.
