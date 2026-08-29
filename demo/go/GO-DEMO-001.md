---
id: GO-DEMO-001
title: Keep HTTP handlers thin
scope: department
department: demo
project: null
language: go
severity: medium
tags:
  - architecture
  - handlers
---

# Rule

HTTP handlers should focus on request parsing, response writing, and delegation. Business rules should live in service or store layers according to the project architecture.

# Rationale

The demo projects are intended to show review checks against clear implementation boundaries. Keeping handlers thin makes business-rule review easier and reduces duplicated logic.

# Detection Guidance

Flag handler changes that introduce complex calculations, state transitions, database-specific branching, or policy decisions that belong in service or persistence layers.

# Good Example

```go
order, err := h.service.CreateOrder(ctx, req)
```

# Bad Example

```go
if customer.Tier == "gold" && total > 100 {
	order.Discount = 10
}
```

# Review Comment Guidance

Ask the developer to move business logic into the appropriate service/store layer and keep the handler responsible for HTTP concerns.
