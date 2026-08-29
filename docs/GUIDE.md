# Knowledgebase Guide

## Purpose

This repository stores markdown review rules for the code review agent. It does not store generated PRD or TD summaries.

## Current Demo Layers

The `code-review-demo` repository loads these layers:

1. `common/go`
2. `demo/go`
3. `demo/demo-project/go`

## Adding Rules

Add one markdown file per rule. Keep rule IDs stable because future metrics will use them to track findings, upvotes, downvotes, consumption, and non-consumption.

## Suppressing Rules

If a rule does not apply to a target repository, add its ID to `knowledge.disabled_rules` in that repo's `.code-review.yml`.

Suppressions should be rare and intentional. Prefer improving or narrowing the rule when it is too broad for multiple repos.
