---
id: GO-COM-001
title: Return errors with enough context
scope: common
department: null
project: null
language: go
severity: medium
tags:
  - errors
  - observability
---

# Rule

When returning an error from a lower-level operation, preserve the original error and add enough context for debugging.

# Rationale

CI review comments should encourage production-friendly error handling. Bare errors make failures harder to trace across handlers, services, repositories, and external dependencies.

# Detection Guidance

Look for returned errors from database, cache, HTTP, file, or encoding operations. Flag cases where the code drops the original error or returns a generic error without operation context.

# Good Example

```go
if err != nil {
	return fmt.Errorf("create product: %w", err)
}
```

# Bad Example

```go
if err != nil {
	return errors.New("failed")
}
```

# Review Comment Guidance

Ask the developer to wrap the original error with operation-specific context. Mention the function or dependency call that produced the error when possible.
