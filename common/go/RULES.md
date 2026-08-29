# Common Go Rules

Company-wide Go rules loaded by default for Go repositories.

## [Return errors with enough context](#return-errors-with-context)

| Field | Value |
| --- | --- |
| ID | `GO-COM-001` |
| Slug | `return-errors-with-context` |
| Contributor | `example@gmail.com` |
| Severity | `P2` |
| Tags | `errors`, `observability` |
| References | None |

### Rule

When returning an error from a lower-level operation, preserve the original error and add enough context for debugging.

This rule applies to error values returned to callers or logged for operators. It does not require exposing internal lower-level error details in user-facing HTTP response bodies.

### Background

Go services often pass errors across handlers, services, repositories, and external dependencies. Review findings are more useful when the resulting code preserves the original failure and explains what operation failed.

### Risks

- Correctness risk: generic errors can hide the failing dependency or operation.
- Observability risk: logs and traces become harder to diagnose during incidents.
- Maintenance risk: future reviewers may need to reproduce issues locally to understand the failure path.

### Review Checklist

- Check database, cache, HTTP, file, and encoding operations.
- Flag returned errors that drop the original error.
- Flag generic errors that do not identify the failed operation.
- Prefer wrapping with `%w` when the caller may need to inspect the original error.
- Do not flag sanitized HTTP response messages such as `writeError(w, http.StatusInternalServerError, "failed to fetch products")` unless the code also drops the lower-level error from returned or logged application errors.

### Good Example

```go
if err != nil {
	return fmt.Errorf("create product: %w", err)
}
```

### Bad Example

```go
if err != nil {
	return errors.New("failed")
}
```

### Review Comment Guidance

Ask the developer to wrap the original error with operation-specific context when returning or logging an application error. Do not ask them to leak internal error details to API clients.
