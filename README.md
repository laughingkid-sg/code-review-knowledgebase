# Code Review Knowledgebase

Markdown rule repository for the intelligent code review demo.

This repository stores reusable review knowledge only. PRD and TD summaries are generated during a pull request run in the implementation repository and uploaded as CI artifacts; they are not stored here.

## Layers

Rules are organized by scope and language:

```text
common/
  go/
demo/
  go/
  demo-project/
    go/
docs/
```

- `common/go`: company-wide Go rules.
- `demo/go`: department-level Go rules for the demo department.
- `demo/demo-project/go`: project-level Go rules for `code-review-demo`.

Target repositories decide which layers to load in their `.code-review.yml`.

## Rule IDs

Use stable rule IDs so findings can be tracked, disabled, counted, and improved over time.

Suggested prefixes:

- `GO-COM-###`: common Go rules.
- `GO-DEMO-###`: demo department Go rules.
- `GO-DEMO-PROJ-###`: demo project Go rules.

## Rule Format

Each rule is a markdown file with front matter:

```markdown
---
id: GO-COM-001
title: Always close HTTP response bodies
scope: common
department: null
project: null
language: go
severity: medium
tags:
  - resource-management
---

# Rule

Describe the rule.

# Rationale

Explain why the rule matters.

# Detection Guidance

Describe what the reviewer should inspect.

# Good Example

```go
defer resp.Body.Close()
```

# Bad Example

```go
resp, _ := http.Get(url)
_ = resp
```

# Review Comment Guidance

Explain how the finding should be written to the developer.
```

## Disabled Rules

Rules can be disabled by ID in a target repository config when a broader rule intentionally does not apply to that repo.
