# Performance Playbook

For performance reviews, tuning plans, and scalability guidance.

## A. Rendering performance priorities

1. Stabilize React inputs passed to `<ReactFlow />`.
2. Reduce subscription breadth for frequently changing state.
3. Lower node/edge visual complexity in large graphs.
4. Limit active graph surface (collapse or hide non-critical branches).

## B. Memoization strategy

Wrap every custom node and edge with `React.memo`. Memoize callbacks and objects:

```tsx
const MyNode = React.memo(({ data }: NodeProps<MyNodeData>) => {
  return <div className="custom-node">{data.label}</div>;
});

// In parent or flow setup:
const onNodeClick = useCallback((_, node: Node) => {
  console.log('clicked', node.id);
}, []);

const nodeTypes = useMemo(() => ({ custom: MyNode }), []);
```

Key rule: `nodeTypes` and `edgeTypes` must be stable references — define outside the component or wrap in `useMemo`. Recreating them causes full remount of all nodes.

## C. Store subscription strategy

```tsx
// BAD — subscribes to entire nodes array, rerenders on any node change
const nodes = useStore((s) => s.nodes);

// GOOD — narrow selector with equality check
const selectedIds = useStore(
  (s) => s.nodes.filter((n) => n.selected).map((n) => n.id),
  (a, b) => a.length === b.length && a.every((id, i) => id === b[i]),
);
```

- Never read full `nodes`/`edges` in components that rerender often.
- Extract computed slices into dedicated selectors with equality functions.

## D. Interaction hotspot checks

Benchmark explicitly:
- Zoom/pan with `panOnScroll` enabled.
- Drag selection with different `selectNodesOnDrag` settings.
- Connection interactions using `onConnectEnd` and validation callbacks.

Cross-check recent release notes for hotspot fixes or regressions.

## E. Visual and layout cost controls

- Limit heavy shadows, complex SVG filters, and layered animations at scale.
- Use progressive disclosure (`hidden` or grouped nodes) for deep trees.
- Precompute layout where possible; avoid full re-layout on every minor edit.

## F. Performance audit checklist

- [ ] Baseline measured with reproducible scenario and graph size.
- [ ] Rerender sources identified (which component, which subscription).
- [ ] Top 3 bottlenecks mapped to concrete code-level mitigations.
- [ ] `nodeTypes`/`edgeTypes` reference stability verified.
- [ ] Risks listed (UX trade-offs, stale data risk, complexity impact).
- [ ] Follow-up metrics defined (FPS, interaction latency, rerender count).
