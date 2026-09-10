---
name: react-flow-advanced-best-practices
description: "基于官方来源与项目实际版本，为 React Flow（@xyflow/react）的架构、性能、TypeScript、自定义节点与边、布局、连接、迁移、测试和可访问性提供建议与实现。用户要求非简单的 React Flow 开发或评审时使用。不用于无 React Flow 的一般 React 页面、普通流程图绘制或无关前端修改。"
---

# React Flow Advanced Best Practices

Produce version-aware, evidence-backed React Flow guidance.
Skip beginner setup unless explicitly requested.

## Workflow

### 1) Refresh official sources

通过脚本绝对路径运行。默认缓存写入 Skill 的 references 目录；只读安装或不希望修改 Skill 时，用 `--output-md` 与 `--output-json` 指定任务目录，并在后续读取该目录的快照。

```bash
python3 "<当前 Skill 绝对目录>/scripts/sync_react_flow_sources.py"
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
