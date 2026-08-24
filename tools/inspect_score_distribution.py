# tools/inspect_score_distribution.py
"""
raw_score 분포를 확인하고, sigmoid 정규화 파라미터(midpoint, steepness) 후보를
시뮬레이션해보는 진단 스크립트. (제출물이 아니라 개발자가 직접 실행하는 도구)
"""

import statistics
from collections import Counter
from pathlib import Path

from ossp_router.protocol import load_input
from ossp_router.heuristic import extract_features, complexity_score, normalize_complexity_score


def inspect(inputs_path, label):
    """1단계: raw_score 분포 확인"""
    batch = load_input(Path(inputs_path))
    raw_scores = [complexity_score(extract_features(ep)) for ep in batch.episodes]

    print(f"\n=== {label} raw_score 분포 (n={len(raw_scores)}) ===")
    print("min:", min(raw_scores))
    print("max:", max(raw_scores))
    print("평균:", statistics.mean(raw_scores))
    print("표준편차:", statistics.pstdev(raw_scores))
    print("중앙값:", statistics.median(raw_scores))

    dist = Counter(raw_scores)
    for k in sorted(dist):
        print(f"  raw_score={k}: {dist[k]}개")

    return raw_scores


def simulate_normalization(raw_scores, midpoint, steepness, label):
    """3단계: 특정 파라미터로 정규화했을 때 분포가 어떻게 되는지 시뮬레이션"""
    normed = [
        normalize_complexity_score(r, midpoint=midpoint, steepness=steepness)
        for r in raw_scores
    ]

    print(f"\n--- {label} (midpoint={midpoint}, steepness={steepness:.3f}) ---")
    print("normalized 평균:", statistics.mean(normed))
    print("normalized 표준편차:", statistics.pstdev(normed))

    bins = [0] * 10
    for n in normed:
        idx = min(9, int(n * 10))
        bins[idx] += 1
    for i, c in enumerate(bins):
        print(f"  [{i/10:.1f}-{(i+1)/10:.1f}): {c}개")


def main():
    # 1단계: 실제 raw_score 분포 확인
    raw_scores = inspect("data/train/inputs-base.json", "Train")  # 실제 파일 경로로 수정

    # 2단계: 분포 통계로 새 파라미터 후보 계산
    mean = statistics.mean(raw_scores)
    std = statistics.pstdev(raw_scores)
    new_midpoint = mean
    new_steepness = 1.5 / max(std, 0.5)   # 표준편차가 너무 작을 때 0으로 나누는 것 방지

    # 3단계: 기존 파라미터 vs 새 파라미터 비교 시뮬레이션
    simulate_normalization(raw_scores, midpoint=4.0, steepness=0.75, label="기존 파라미터")
    simulate_normalization(raw_scores, midpoint=new_midpoint, steepness=new_steepness, label="새 파라미터 후보")

    print(f"\n추천 파라미터: midpoint={new_midpoint:.4f}, steepness={new_steepness:.4f}")


if __name__ == "__main__":
    main()