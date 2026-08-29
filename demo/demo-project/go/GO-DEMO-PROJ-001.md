---
id: GO-DEMO-PROJ-001
title: Keep demo APIs aligned with PRD and TD documents
scope: project
department: demo
project: demo-project
language: go
severity: high
tags:
  - business-logic
  - documentation
---

# Rule

Changes to demo API behavior must remain consistent with the relevant `docs/PRD.md` and `docs/TDD.md` for the affected demo project.

# Rationale

The central demo requirement is to compare implementation logic against product and technical requirements. This project-level rule gives the agent a stable reason to inspect PRD and TD summaries for every pull request.

# Detection Guidance

For changed files under `demo-projects/simple-api` or `demo-projects/medium-api`, identify the matching document set from `.code-review.yml`. Compare changed handler, service, repository, and model behavior against that project's PRD and TD summary artifact.

# Good Example

```go
if req.Price <= 0 {
	return ErrInvalidPrice
}
```

# Bad Example

```go
product.Price = req.Price
```

# Review Comment Guidance

Reference the affected PRD or TD requirement in plain language, then explain the implementation mismatch and required code change.
