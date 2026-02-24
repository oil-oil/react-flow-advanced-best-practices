# Version Watchlist

Use this file to keep recommendations aligned with current React Flow releases.
Always refresh with `scripts/sync_react_flow_sources.py` before making claims.

## Baseline protocol

1. Read `references/react-flow-latest-snapshot.md`.
2. Confirm latest `@xyflow/react` release date and tag.
3. Check docs "Last updated" timestamps for the pages you cite.
4. Include absolute dates in final guidance.

## High-impact checks

- API rename/deprecation exposure in legacy code (for example `onEdgeUpdate` -> `onReconnect`).
- Hook evolution (`useHandleConnections` vs `useNodeConnections`).
- Type changes affecting custom node/edge typing and `useNodesData` narrowing.
- New rendering controls (for example `zIndexMode`) that alter layering behavior.
- Performance patches that can change perceived responsiveness.

## Release triage format

Use this exact triage format in audits:

- Current package target:
- Latest official package tag:
- Time delta between target and latest:
- Potentially relevant release notes:
- Required migration or validation actions:

Example (filled):

- Current package target: @xyflow/react@12.9.2
- Latest official package tag: @xyflow/react@12.10.1
- Time delta: ~2 months behind
- Potentially relevant release notes:
  - 12.10.0: `zIndexMode` prop added — may affect layering if using custom z-index logic
  - 12.10.0: `experimental_useOnNodesChangeMiddleware` — new hook, no action needed unless adopting
  - 12.10.1: `useNodesData` return type narrowed — check custom type guards
- Required migration or validation actions:
  - Review any manual z-index manipulation against new `zIndexMode` behavior
  - Verify `useNodesData` consumers still compile after type narrowing

## Escalation rule

If release notes and docs disagree:

- Trust release notes for package-level behavior changes.
- Trust docs for usage patterns and implementation guidance.
- Call out the discrepancy explicitly and provide both source links.
