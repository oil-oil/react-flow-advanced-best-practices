# Advanced Feature Playbook

Answer architecture and advanced capability questions.
Skip beginner guidance unless explicitly requested.

## 1) Computing flows

Two-stage pattern:

1. Write node output with `updateNodeData`.
2. Read upstream data with `useNodeConnections` + `useNodesData`.

```tsx
function ProcessorNode({ id }: NodeProps) {
  const connections = useNodeConnections({ type: 'target' });
  const inputData = useNodesData(connections.map((c) => c.source));
  const { updateNodeData } = useReactFlow();

  useEffect(() => {
    const result = compute(inputData);
    updateNodeData(id, { output: result });
  }, [inputData]);

  return <div>{/* ... */}</div>;
}
```

Rules:
- Model `data` as typed domain payload, not UI-only state.
- Partition by handle when a node has multi-input semantics.
- Prevent feedback loops: define compute order, keep updates idempotent.
- Prefer narrow subscriptions to connected nodes over global graph scans.

## 2) SSR / SSG

- Provide node dimensions on server (`width`/`height` or `initialWidth`/`initialHeight`).
- Provide handle positions when rendering edges server-side.
- Use server `fitView` only when viewport framing must be deterministic at first paint.
- Validate hydration: layout may differ between server and client.

## 3) Multiplayer collaboration

Split state: durable (topology, data, positions) vs ephemeral (selection, hover).

- Choose conflict strategy first (CRDT or server-authoritative).
- Keep transport payloads schema-stable and patch-oriented.
- Avoid syncing high-frequency ephemeral state unless UX requires it.

## 4) Whiteboard capabilities

- Lasso, eraser, rectangle coexist with workflow editing.
- Gate freehand features by product tier (Pro dependency awareness).
- Define explicit interaction mode transitions to avoid accidental edits.

## 5) Layout and sub-flows

Engine selection by graph characteristics:

- Dagre: quick hierarchical layout; watch documented sub-flow caveats.
- D3 force/hierarchy: dynamic or tree-biased use cases.
- ELK: highest control for complex constraints, higher complexity cost.

Sub-flow rules:
- Keep parent-child semantics explicit through `parentId`.
- Validate edge z-order and interaction behavior in nested flows.

## 6) TypeScript

Type custom nodes and edges explicitly to get narrowed `data` in hooks:

```tsx
type TextNode = Node<{ label: string }, 'text'>;
type NumberNode = Node<{ value: number }, 'number'>;
type AppNode = TextNode | NumberNode;

// useNodesData narrows by checking node.type
const data = useNodesData<AppNode>(nodeIds);
data.forEach((d) => {
  if (d.type === 'text') d.data.label; // string
});
```

Rules:
- Define a union type for all node variants; pass it as generic to hooks.
- Use `NodeProps<T>` in custom node components for type-safe `data` access.
- Avoid `any` on edge/node data — it defeats the purpose of typed flows.

## 7) Testing

- Use `@testing-library/react` with `ReactFlowProvider` wrapper.
- Mock `getBoundingClientRect` — React Flow relies on DOM measurements.
- Test node interactions via `fireEvent` on node DOM elements, not internal state.
- For integration tests, prefer Playwright/Cypress over unit tests for drag/connect flows.

## 8) Accessibility

- Set `ariaLabel` on `<ReactFlow>` for screen reader context.
- Custom nodes should use semantic HTML (buttons, inputs) not bare divs.
- Keyboard navigation: nodes are focusable by default; ensure custom nodes preserve `tabIndex`.
- Test with screen reader to verify edge announcements and node focus order.

## 9) Controlled vs uncontrolled flows

Decision criteria:
- Controlled (`nodes`/`edges` + `onNodesChange`/`onEdgesChange`): full state ownership, needed for undo/redo, persistence, or external state sync.
- Uncontrolled (`defaultNodes`/`defaultEdges`): simpler setup, React Flow manages state internally.

```tsx
// Controlled — you own the state
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

// Uncontrolled — React Flow owns the state
<ReactFlow defaultNodes={initialNodes} defaultEdges={initialEdges} />
```

Rule: start uncontrolled for prototypes; switch to controlled when you need external state access.

## 10) Upgrade-aware API use

- `useNodeConnections` is the broader hook; `useHandleConnections` has narrower per-handle scope. Both are current API — choose based on granularity needs.
- Watch release notes for performance patches that change pan/zoom/drag behavior.
- Include migration implications when advising on legacy codebases.
- Check `references/version-watchlist.md` for the triage protocol.
