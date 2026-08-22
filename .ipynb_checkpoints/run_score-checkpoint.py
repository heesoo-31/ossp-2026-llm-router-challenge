import json
import sys
from pathlib import Path

# src 경로 등록
sys.path.append("src")

import ossp_router.protocol as protocol
from ossp_router.protocol import (
    load_bundled_policy,
    load_input,
    parse_submission,
)
from ossp_router.scoring import score_submissions


def load_outcomes_file(path: Path):
    """outcomes.json 파일을 protocol 객체에 맞춰 로드"""
    for fn_name in ["load_outcomes", "load_outcome_batch", "load_outcome"]:
        if hasattr(protocol, fn_name):
            return getattr(protocol, fn_name)(path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if hasattr(protocol, "OutcomeBatch"):
        cls = getattr(protocol, "OutcomeBatch")
        if hasattr(cls, "model_validate"):
            return cls.model_validate(data)
        if hasattr(cls, "from_dict"):
            return cls.from_dict(data)
        if hasattr(cls, "parse_obj"):
            return cls.parse_obj(data)
        return cls(**data)
    return data


def main():
    # 1. Inputs, Outcomes, Policy 로드
    inputs = load_input(Path("data/materialized/train/inputs.json"))
    outcomes = load_outcomes_file(Path("data/train/outcomes.json"))
    policy = load_bundled_policy()

    # 2. 3개 티어 제출 파일 로드
    sub_paths = ["sub_fast.json", "sub_balanced.json", "sub_premium.json"]
    submissions = []
    for p in sub_paths:
        with open(p, "r", encoding="utf-8") as f:
            submissions.append(parse_submission(json.load(f)))

    # 3. 채점 수행 및 JSON 리포트 출력
    report = score_submissions(inputs, outcomes, submissions, policy)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()