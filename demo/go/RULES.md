# Demo Department Go Rules

Department-level Go rules for the demo department.

## GO-DEMO-001: keep-http-handlers-thin - Keep HTTP handlers thin

| Field | Value |
| --- | --- |
| Owner | `example@gmail.com` |
| Contributor | `example@gmail.com` |
| Level | `recommended` |
| Severity | `medium` |
| Tags | `architecture`, `handlers` |
| References | None |

### Rule

HTTP handlers should focus on request parsing, response writing, and delegation. Domain logic should live in service or store layers according to the project architecture.

### Background

The demo projects use handlers, services, stores, and repositories to keep HTTP transport code separate from domain behavior. Keeping these boundaries clear makes code-rule review more precise and keeps handler tests focused.

### Risks

- Correctness risk: duplicated handler logic can drift from service-layer behavior.
- Maintainability risk: handlers become harder to test and reuse.
- Review risk: code-rule checks become less reliable when domain behavior is spread across HTTP glue code.

### Review Checklist

- Check whether changed handlers perform calculations, state transitions, or policy decisions.
- Check whether validation belongs in the handler or the service layer.
- Prefer delegating domain decisions to a service or store method that can be unit tested.

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

Ask the developer to move domain logic into the appropriate service/store layer and keep the handler responsible for HTTP concerns.
