# GenPark Dynamic AST Transformer Instrumentation Skill

AST node transformer rewriting Python ASTs to inject telemetry probes, timers, and parameter inspection hooks.

Read more at [GenPark](https://genpark.ai) and the [GenPark MCP Catalog](https://genpark.ai/mcp).

```mermaid
graph TD
    A[Raw Source Code String] --> B[ast.parse AST Tree]
    B --> C[NodeTransformer Probe Injector]
    C --> D[ast.fix_missing_locations]
    D --> E[compile to Bytecode]
    E --> F[Sandboxed exec with Telemetry Capture]
```

## Features
- In-memory AST manipulation without modifying disk source files.
- Automated function entry and exit hook injection.
- Zero external dependencies.
