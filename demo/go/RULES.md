# Demo Department Go Rules

Department-level Go rules for the demo department.

## GO-DEMO-001: Keep HTTP handlers thin

| Field | Value |
| --- | --- |
| Slug | `keep-http-handlers-thin` |
| Scope | `department` |
| Department | `demo` |
| Language | `go` |
| Owner | `demo` |
| Contributor | `codex` |
| Level | `recommended` |
| Severity | `medium` |
| Tags | `architecture`, `handlers` |
| References | None |

### Rule

HTTP handlers should focus on request parsing, response writing, and delegation. Business rules should live in service or store layers according to the project architecture.

### Background

The demo projects are designed to make business logic review possible across simple and medium Go APIs. Keeping HTTP concerns separate from business rules makes it easier for the agent to compare implementation logic against PRD and TD requirements.

### Risks

- Correctness risk: duplicated handler logic can drift from service-layer behavior.
- Maintainability risk: handlers become harder to test and reuse.
- Review risk: business-rule checks become less reliable when policy is spread across HTTP glue code.

### Review Checklist

- Check whether changed handlers perform calculations, state transitions, or policy decisions.
- Check whether validation belongs in the handler or the service layer.
- Prefer delegating business decisions to a service or store method that can be unit tested.

### Good Example

```go
order, err := h.service.CreateOrder(ctx, req)
```

### Bad Example

```go
if customer.Tier == "gold" && total > 100 {
	order.Discount = 10
}
```

### Review Comment Guidance

Ask the developer to move business logic into the appropriate service/store layer and keep the handler responsible for HTTP concerns.
