import json
from pathlib import Path

from ossp_router.data_prep import load_episode_table, light_baseline_total, cost_ratio
from ossp_router.threshold_search import (
    optimize_all_tiers,
    derive_thresholds_fast,
    verify_and_tighten,
    assign_by_threshold,
    OFFICIAL_LIMIT,
    SAFETY_TARGET,
)
from ossp_router.heuristic import get_prompt_score


def tune_on_train(train_rows):
    baseline_total = light_baseline_total(train_rows)
    opt_results = optimize_all_tiers(train_rows)
    final = {}
    for tier, res in opt_results.items():
        t1, t2 = derive_thresholds_fast(train_rows, res["assignment"])
        t1, t2, ratio = verify_and_tighten(train_rows, t1, t2, tier, baseline_total)
        final[tier] = {"t1": t1, "t2": t2, "train_ratio": ratio}
        print(f"[Train/{tier:9s}] t1={t1:.4f} t2={t2:.4f} ratio={ratio:.4f} "
              f"(safety_target={SAFETY_TARGET[tier]}, official_limit={OFFICIAL_LIMIT[tier]})")
    return final


def validate_on_dev(dev_rows, thresholds):
    baseline_total = light_baseline_total(dev_rows)
    report = {}
    print("\n--- Dev 검증 ---")
    for tier, th in thresholds.items():
        assignment = {
            r["episode_id"]: assign_by_threshold(r["score"], th["t1"], th["t2"])
            for r in dev_rows
        }
        ratio = cost_ratio(dev_rows, assignment, baseline_total)
        if ratio > OFFICIAL_LIMIT[tier]:
            flag = "FAIL(공식한도 초과)"
        elif ratio > SAFETY_TARGET[tier]:
            flag = "WARN(안전유격 벗어남)"
        else:
            flag = "OK"
        report[tier] = {"dev_ratio": ratio, "status": flag}
        print(f"[Dev/{tier:9s}] ratio={ratio:.4f} target={SAFETY_TARGET[tier]} -> {flag}")
    return report


def print_distribution(rows, thresholds, label):
    from collections import Counter
    print(f"\n--- {label} 모델 분포 ---")
    for tier, th in thresholds.items():
        assignment = [assign_by_threshold(r["score"], th["t1"], th["t2"]) for r in rows]
        dist = Counter(assignment)
        print(f"  {tier:9s}: {dict(dist)}")


def main():
    train_rows = load_episode_table(
        "data/materialized/train/inputs.json",
        "data/train/outcomes.json",
        score_fn=get_prompt_score,
    )
    thresholds = tune_on_train(train_rows)
    print_distribution(train_rows, thresholds, "Train")

    dev_rows = load_episode_table(
        "data/materialized/dev/inputs.json",
        "data/dev/outcomes.json",
        score_fn=get_prompt_score,
    )
    dev_report = validate_on_dev(dev_rows, thresholds)
    print_distribution(dev_rows, thresholds, "Dev")

    output = {
        "thresholds": {tier: {"t1": v["t1"], "t2": v["t2"]} for tier, v in thresholds.items()},
        "train_ratio": {tier: v["train_ratio"] for tier, v in thresholds.items()},
        "dev_report": dev_report,
    }
    out_path = Path("build/tuned_thresholds.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n결과 저장: {out_path}")

    failed = [tier for tier, r in dev_report.items() if "FAIL" in r["status"]]
    if failed:
        print(f"\n주의: Dev에서 공식 한도를 초과한 tier가 있습니다: {failed}")


if __name__ == "__main__":
    main()