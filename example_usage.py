"""
Demonstration of Dynamic AST Transformer Instrumentation Skill
"""

from client import CodeInstrumenter

def main():
    print("=== Instrumenting Python Code via Dynamic AST Transformation ===")
    instrumenter = CodeInstrumenter()

    sample_code = """
def compute_factorial(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res
"""

    print("Source Code to Instrument:")
    print(sample_code)

    result = instrumenter.instrument_and_exec(sample_code, "compute_factorial", 5)
    print(f"Execution Result: compute_factorial(5) = {result}")

    print("\nCaptured Telemetry Events:")
    for ev in instrumenter.probe.events:
        print(f"  [{ev['event']}] Function: {ev['function']} | Data: {ev.get('args') or ev.get('result')}")

    assert result == 120
    assert len(instrumenter.probe.events) == 2
    print("AST Transformer Instrumentation Verification PASS!")

if __name__ == "__main__":
    main()
