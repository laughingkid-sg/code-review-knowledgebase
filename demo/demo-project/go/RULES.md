# Demo Project Go Rules

Project-level Go rules for `code-review-demo`.

## GO-DEMO-PROJ-001: Do not continue after request binding or decode failures

| Field | Value |
| --- | --- |
| Slug | `stop-after-request-binding-failure` |
| Scope | `project` |
| Department | `demo` |
| Project | `demo-project` |
| Language | `go` |
| Owner | `demo-project` |
| Contributor | `codex` |
| Level | `required` |
| Severity | `high` |
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
