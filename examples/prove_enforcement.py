import json
import sys
from pathlib import Path

# Add spec2viz to path if running from this directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from spec2viz import load, compile_ir

def prove_enforcement():
    # 1. Load the reflection spec
    # It defines api -> core (uses)
    spec_path = Path(__file__).parent / "reflection" / "canonical.yml"
    diagram = load(spec_path)
    
    # 2. Compile to enforcement artifact
    artifact = compile_ir(diagram)
    
    # 3. Extract allowed 'uses' dependencies from facts
    allowed_uses = set()
    for fact in artifact.facts:
        if fact.relation == "uses":
            allowed_uses.add((fact.source, fact.target))
            
    # 4. Simulate detected imports in code
    detected_imports = [
        ("api", "core"),  # Matches spec
        ("core", "api"),  # Violation!
    ]
    
    print("## Architecture Enforcement Proof")
    print(f"Source Spec: {spec_path.name}")
    print(f"Artifact Fingerprint: {artifact.fingerprint[:12]}...")
    print("-" * 40)
    
    violations = 0
    for source, target in detected_imports:
        if (source, target) in allowed_uses:
            print(f"  [PASS] {source} -> {target}")
        else:
            print(f"  [FAIL] {source} -> {target} (Violation: unexpected inward dependency)")
            violations += 1
            
    print("-" * 40)
    if violations > 0:
        print(f"RESULT: Enforcement FAILED with {violations} violations.")
    else:
        print("RESULT: Enforcement PASSED.")

if __name__ == "__main__":
    prove_enforcement()
