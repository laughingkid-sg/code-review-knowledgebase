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
func (h *OrderHandler) CreateOrder(c *gin.Context) {
	var req CreateOrderRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, errorResponse(err))
		return
	}

	order, err := h.service.CreateOrder(c.Request.Context(), req)
	if err != nil {
		c.JSON(statusFromError(err), errorResponse(err))
		return
	}

	c.JSON(http.StatusCreated, order)
}
```

### Bad Example

```go
func (h *OrderHandler) CreateOrder(c *gin.Context) {
	var req CreateOrderRequest
	_ = c.ShouldBindJSON(&req)

	total := 0
	for _, item := range req.Items {
		total += item.Quantity * item.UnitPrice
	}

	order := model.Order{
		CustomerID: req.CustomerID,
		Total:      total,
		Status:     "pending",
	}

	_ = h.repository.Save(c.Request.Context(), order)
	c.JSON(http.StatusCreated, order)
}
```

### Review Comment Guidance

Ask the developer to move business logic into the appropriate service/store layer and keep the handler responsible for HTTP concerns.
