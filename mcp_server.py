"""
MCP Server for Dynamic AST Transformer Instrumentation Skill
"""

import json
import sys
from client import CodeInstrumenter

def handle_call(name: str, args: dict) -> dict:
    if name == "instrument_and_run":
        src = args.get("source_code", "")
        func_name = args.get("func_name", "")
        params = args.get("params", [])
        inst = CodeInstrumenter()
        try:
            res = inst.instrument_and_exec(src, func_name, *params)
            return {"result": res, "telemetry": inst.probe.events}
        except Exception as e:
            return {"error": str(e)}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
