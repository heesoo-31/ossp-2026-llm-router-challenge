import json
from pathlib import Path
from ossp_router.protocol import load_input, load_bundled_policy
from ossp_router.router import generate_route_predictions

def build_all_submissions():
    input_path = Path("data/materialized/dev/inputs.json")
    output_dir = Path("build/dev-submission")
    output_dir.mkdir(parents=True, exist_ok=True)

    inputs = load_input(input_path)
    
    # 공식 정책(policy) 객체에서 정확한 policy_id 동적 추출
    try:
        policy = load_bundled_policy()
        policy_id = getattr(policy, "policy_id", "ossp-2026-prompt-router-v1")
        if isinstance(policy, dict):
            policy_id = policy.get("policy_id", policy_id)
    except Exception:
        policy_id = "ossp-2026-prompt-router-v1"

    challenge_id = getattr(inputs, "challenge_id", "ossp-2026-llm-router-challenge")
    schema_version = getattr(inputs, "schema_version", 1)
    split = getattr(inputs, "split", "dev")
    
    if isinstance(inputs, dict):
        challenge_id = inputs.get("challenge_id", challenge_id)
        schema_version = inputs.get("schema_version", schema_version)
        split = inputs.get("split", split)

    for tier in ["fast", "balanced", "premium"]:
        decisions = generate_route_predictions(inputs, tier)
        
        if not decisions and input_path.exists():
            with open(input_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            decisions = generate_route_predictions(raw_data, tier)

        submission_data = {
            "challenge_id": challenge_id,
            "schema_version": schema_version,
            "split": split,
            "tier": tier,
            "policy_id": policy_id,
            "decisions": decisions
        }
        
        out_file = output_dir / f"{tier}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(submission_data, f, indent=2, ensure_ascii=False)
            
        print(f"[SUCCESS] {tier}.json 생성 완료 (policy_id: {policy_id})")

if __name__ == "__main__":
    build_all_submissions()