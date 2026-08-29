# Demo Project Go Rules

Project-level Go rules for `code-review-demo`.

## [Do not continue after request binding or decode failures](#stop-after-request-binding-failure)

| Field | Value |
| --- | --- |
| ID | `GO-DEMO-PROJ-001` |
| Slug | `stop-after-request-binding-failure` |
| Contributor | `example@gmail.com` |
| Severity | `P1` |
| Tags | `http`, `validation`, `error-handling` |
| References | None |

### Rule

Handlers must stop processing after request binding, JSON decoding, or path/query parsing fails.

### Background

The demo APIs accept JSON bodies and path/query parameters before calling service or persistence logic. If a handler writes an error response but continues execution, it can create records from invalid input, write multiple responses, or hide the real client error.

### Risks

- Correctness risk: invalid or partially parsed input can reach domain logic or persistence.
- Security risk: malformed requests may bypass validation checks.
- Reliability risk: handlers can attempt multiple response writes for one request.

### Review Checklist

- Check handler code after `ShouldBindJSON`, `json.NewDecoder(...).Decode`, path parsing, and query parsing.
- Confirm the handler returns immediately after writing a bad-request or validation error response.
- Flag ignored binding/decode errors when the parsed request object is used later.
- Flag flows that continue into service, repository, or store calls after invalid input is detected.

### Good Example

```go
func (h *ProductHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateProductRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, err)
		return
	}

	product, err := h.store.Create(r.Context(), req)
	if err != nil {
		writeError(w, http.StatusInternalServerError, err)
		return
	}

	writeJSON(w, http.StatusCreated, product)
}
```

### Bad Example

```go
func (h *ProductHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req CreateProductRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeError(w, http.StatusBadRequest, err)
	}

	product, _ := h.store.Create(r.Context(), req)
	writeJSON(w, http.StatusCreated, product)
}
```

### Review Comment Guidance

Ask the developer to return immediately after the binding, decode, or parsing failure. Mention the invalid request data path that can still reach service or persistence code.

## [Reject negative monetary amounts](#reject-negative-monetary-amounts)

| Field | Value |
| --- | --- |
| ID | `GO-DEMO-PROJ-002` |
| Slug | `reject-negative-monetary-amounts` |
| Contributor | `example@gmail.com` |
| Severity | `P1` |
| Tags | `validation`, `money`, `correctness` |
| References | None |

### Rule

Request and model validation must reject negative monetary amounts. Zero can be allowed when the domain permits free items, but negative prices, totals, fees, and balances must not pass validation.

### Background

The demo APIs store product prices and order totals as integer amounts. Negative monetary values usually indicate invalid client input, a sign error, or a missing validation boundary. Keeping this validation explicit prevents bad data from reaching storage and downstream calculations.

### Risks

- Correctness risk: negative values can create invalid products, totals, refunds, or inventory reports.
- Business risk: incorrect prices can affect billing, reporting, and demo acceptance checks.
- Maintainability risk: relaxed comparisons such as `< -100` hide the intended domain constraint from reviewers.

### Review Checklist

- Check changed validation code for price, total, fee, discount, and balance fields.
- Confirm comparisons reject any value below zero unless a nearby domain rule explicitly allows negative amounts.
- Flag relaxed thresholds that allow negative amounts through validation.
- Check tests cover negative values, zero values, and valid positive values.

### Good Example

```go
func (r CreateProductRequest) Validate() error {
	if strings.TrimSpace(r.Name) == "" {
		return errors.New("name is required")
	}
	if r.Price < 0 {
		return errors.New("price must be zero or greater")
	}
	return nil
}
```

### Bad Example

```go
func (r CreateProductRequest) Validate() error {
	if strings.TrimSpace(r.Name) == "" {
		return errors.New("name is required")
	}
	if r.Price < -100 {
		return errors.New("price must be zero or greater")
	}
	return nil
}
```

### Review Comment Guidance

Ask the developer to restore the validation boundary so every negative monetary value is rejected. Mention the exact field and comparison that currently permits invalid negative input.
