import numpy as np
from .data_prep import MODELS, light_baseline_total, cost_ratio

OFFICIAL_LIMIT = {"fast": 1.25, "balanced": 2.00, "premium": 4.00}
SAFETY_TARGET = {"fast": 1.20, "balanced": 1.90, "premium": 3.80}

def efficient_options(quality: dict, cost: dict):
    opts = sorted([(cost[m], quality[m], m) for m in MODELS], key=lambda x: x[0])
    frontier = []
    best_q = -1e18
    for c, q, m in opts:
        if q > best_q:
            frontier.append((c, q, m))
            best_q = q
    return frontier

def pick_for_lambda(frontier, lam):
    return max(frontier, key=lambda o: o[1] - lam * o[0])

def solve_budget(rows, target_ratio, baseline_total, lam_lo=0.0, lam_hi=1e6, iters=60):
    frontiers = {r["episode_id"]: efficient_options(r["quality"], r["cost"]) for r in rows}
    target_cost = target_ratio * baseline_total

    def total_cost_for_lambda(lam):
        return sum(pick_for_lambda(frontiers[eid], lam)[0] for eid in frontiers)
    
    lo, hi = lam_lo, lam_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        c =total_cost_for_lambda(mid)
        if c > target_cost:
            lo = mid
        else:
            hi = mid
    lam_star = hi

    assignment = {eid: pick_for_lambda(frontiers[eid], lam_star)[2] for eid in frontiers}
    return assignment, lam_star

def optimize_all_tiers(rows):
    baseline_total = light_baseline_total(rows)
    results = {}
    for tier, target in SAFETY_TARGET.items():
        assignment, lam = solve_budget(rows, target, baseline_total)
        actual_ratio = cost_ratio(rows, assignment, baseline_total)
        results[tier] = {"assignment": assignment, "lambda": lam, "train_ratio": actual_ratio}
    return results

def derive_thresholds_fast(rows, assignment, n_bins=200):
    rank = {"ax31-light": 0, "ax31": 1, "axk1-think": 2}
    scores = np.array([r["score"] for r in rows])
    labels = np.array([rank[assignment[r["episode_id"]]] for r in rows])

    candidates = np.unique(np.quantile(scores, np.linspace(0, 1, n_bins)))
    best_t1, best_t2, best_matched = None, None, -1
    for t1 in candidates:
        for t2 in candidates[candidates > t1]:
            pred = np.where(scores < t1, 0, np.where(scores < t2, 1, 2))
            matched = (pred == labels).sum()
            if matched > best_matched:
                best_t1, best_t2, best_matched = t1, t2, matched
    return float(best_t1), float(best_t2)

def assign_by_threshold(score, t1, t2):
    if score <t1:
        return "ax31-light"
    elif score < t2:
        return "ax31"
    else:
        return "axk1-think"
    
def verify_and_tighten(rows, t1, t2, tier, baseline_total, max_search=50):
    official = OFFICIAL_LIMIT[tier]
    safety = SAFETY_TARGET[tier]

    def ratio_for(t1_, t2_):
        assignment = {r["episode_id"]: assign_by_threshold(r["score"], t1_, t2_) for r in rows}
        return cost_ratio(rows, assignment, baseline_total)

    r = ratio_for(t1, t2)
    step = 0
    while r > safety and step < max_search:
        t1 = min(t1 * 1.02 + 1e-6, 1.0)
        t2 = min(t2 * 1.02 + 1e-6, 1.0)
        r = ratio_for(t1, t2)
        step += 1

    assert r <= official, f"{tier}: 여전히 공식 한도 초과 (ratio={r:.3f})"
    return t1, t2, r
