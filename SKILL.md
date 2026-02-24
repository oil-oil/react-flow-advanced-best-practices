---
name: react-flow-advanced-best-practices
description: >
  Expert-level React Flow (@xyflow/react) guidance covering architecture, performance,
  TypeScript typing, testing, accessibility, computing flows, SSR/SSG, multiplayer,
  whiteboard, layout strategy, custom nodes/edges, handle connections, drag-and-drop,
  migration, and version-aware audits. Use when asked about React Flow / xyflow
  best practices, advanced patterns, performance tuning, custom node/edge design,
  controlled vs uncontrolled flows, or any non-trivial React Flow implementation.
---

# React Flow Advanced Best Practices

Produce version-aware, evidence-backed React Flow guidance.
Skip beginner setup unless explicitly requested.

## Workflow

### 1) Refresh official sources

Run from the skill root directory:

```bash
python3 "$(dirname "$0")/scripts/sync_react_flow_sources.py"
```

Outputs:
- `references/react-flow-latest-snapshot.md` — human-readable baseline for all answers.
- `references/react-flow-latest-snapshot.json` — machine-parseable variant; use when programmatically comparing versions or building migration diffs.

If fetch errors occur, note gaps and continue with available data.

### 2) Load only the needed references

| Request type | Reference file |
|---|---|
| URL routing / "which page?" | `references/source-map.md` |
| Architecture, advanced features | `references/advanced-feature-playbook.md` |
| Performance tuning | `references/performance-playbook.md` |
| Version checks, migration | `references/version-watchlist.md` |

### 3) Generate guidance

- Quote concrete version and date context (docs last-updated + latest `@xyflow/react` tag).
- Tie every recommendation to a specific official page.
- Prefer trade-offs, failure modes, and decision criteria over generic tips.
- Flag deprecated or renamed APIs with source links.
- Separate durable architecture choices from optional enhancements.
- Include short canonical code patterns where they prevent common mistakes.

## Output template

1. Current baseline (version / date)
2. Key decisions and trade-offs
3. Recommended pattern (with code if non-trivial)
4. Performance risks and mitigations
5. Validation checklist
6. Source links

## Non-negotiables

- Official docs and release notes are the source of truth.
- Never rely on memory for fast-changing API details — always refresh first.
- Call out uncertainty explicitly when official sources are silent.
