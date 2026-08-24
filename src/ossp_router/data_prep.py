from pathlib import Path
from typing import Dict

from .protocol import (
    Episode,
    Outcome,
    load_input,
    load_outcomes,
    load_bundled_policy,
    RoutingPolicy,
    MODEL_IDS,
)
from .heuristic import get_prompt_score

MODELS = list(MODEL_IDS)

def compute_cost(outcome: Outcome, policy: RoutingPolicy):
    rates = policy.models[outcome.model_id]
    token_unit = policy.token_unit
    return (
        rates.fixed_cost
        + rates.input_token_rate * outcome.input_tokens / token_unit
        + rates.output_token_rate * outcome.output_tokens / token_unit
    )

def load_episode_table(inputs_path, outcomes_path, score_fn = get_prompt_score, policy=None):
    input_batch = load_input(Path(inputs_path))
    outcome_batch = load_outcomes(Path(outcomes_path))
    policy = policy or load_bundled_policy()

    outcome_by_ep: Dict[str, Dict[str, Outcome]] = {}
    for o in outcome_batch.outcomes:
        outcome_by_ep.setdefault(o.episode_id, {})[o.model_id] = o

    rows = []
    for ep in input_batch.episodes:
        eid = ep.episode_id
        s = score_fn(ep)
        model_outcomes = outcome_by_ep[eid]
        rows.append({
            "episode_id": eid,
            "score": float(s),
            "quality": {m: float(model_outcomes[m].score) for m in MODELS},
            "cost": {m: float(compute_cost(model_outcomes[m], policy)) for m in MODELS},
        })
    return rows

def light_baseline_total(rows):
    return sum(r["cost"]["ax31-light"] for r in rows)

def cost_ratio(rows, assignment, baseline_total):
    total = sum(r["cost"][assignment[r["episode_id"]]] for r in rows)
    return total / baseline_total