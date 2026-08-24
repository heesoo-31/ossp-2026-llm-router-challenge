import re
from typing import Any, List, Dict

def compute_ml1_complexity_score(prompt: str) -> float:
    """ML 1: 프롬프트 텍스트 특징 기반 Prompt Scorer (0.0 ~ 1.0 복잡도 점수 산출)"""
    if not prompt:
        return 0.0

    score = 0.0
    p_len = len(prompt)

    # 1. 문장 길이 스코어링
    if p_len > 1200: score += 0.35
    elif p_len > 600: score += 0.20
    elif p_len > 250: score += 0.10

    # 2. 코드 구조 키워드 검출
    code_matches = len(re.findall(
        r'\b(def|class|function|import|return|for|while|if|else|try|catch|public|struct)\b', 
        prompt, re.IGNORECASE
    ))
    if code_matches >= 4: score += 0.35
    elif code_matches >= 2: score += 0.20

    # 3. 추론 및 수학 수식 검출
    reasoning_matches = len(re.findall(
        r'(\\int|\\sum|\\sqrt|\\frac|=|<=|>=|!=|\b(proof|prove|equation|algorithm|derive|step-by-step|optimize)\b)', 
        prompt, re.IGNORECASE
    ))
    if reasoning_matches >= 3: score += 0.30
    elif reasoning_matches >= 1: score += 0.15

    return min(1.0, score)

def select_model_by_tier(prompt: str, tier: str) -> str:
    """ML 2: Safety Margin(Fast 1.20, Balanced 1.90, Premium 3.80) 기반 Threshold Optimizer"""
    score = compute_ml1_complexity_score(prompt)

    if tier == "fast":
        # Fast (목표 1.20x / 한도 1.25x): 상위 3% ax31 배차
        return "ax31" if score >= 0.88 else "ax31-light"

    elif tier == "balanced":
        # Balanced (목표 1.90x / 한도 2.00x): 상위 18% ax31 배차하여 1.90x 준수
        if score >= 0.58:
            return "ax31"
        return "ax31-light"

    elif tier == "premium":
        # Premium (목표 3.80x / 한도 4.00x): axk1-think 상위 4.5%, ax31 상위 30% 배차
        if score >= 0.84:
            return "axk1-think"
        elif score >= 0.48:
            return "ax31"
        return "ax31-light"

    return "ax31-light"

def _extract_items(inputs: Any) -> list:
    if inputs is None: return []
    if isinstance(inputs, (list, tuple)): return list(inputs)
    if isinstance(inputs, dict):
        for key in ["episodes", "requests", "items", "prompts", "samples", "data", "inputs"]:
            if key in inputs and isinstance(inputs[key], (list, tuple)):
                return list(inputs[key])
        return list(inputs.values())

    for attr in ["episodes", "requests", "items", "prompts", "samples", "data", "inputs"]:
        if hasattr(inputs, attr):
            val = getattr(inputs, attr)
            if callable(val):
                try: val = val()
                except Exception: pass
            if val is not None:
                try:
                    res = list(val)
                    if res: return res
                except Exception: pass

    if hasattr(inputs, "__dict__"):
        for val in vars(inputs).values():
            if isinstance(val, (list, tuple)) and len(val) > 0:
                return list(val)

    return []

def _extract_id_and_prompt(item: Any, default_idx: int):
    episode_id = None
    prompt = ""

    for id_key in ["episode_id", "id", "item_id", "prompt_id", "request_id"]:
        if isinstance(item, dict) and id_key in item:
            episode_id = item[id_key]
            break
        elif hasattr(item, id_key):
            episode_id = getattr(item, id_key)
            break

    if episode_id is None:
        episode_id = str(default_idx)

    for p_key in ["prompt", "text", "query", "messages", "content", "input"]:
        if isinstance(item, dict) and p_key in item:
            val = item[p_key]
            prompt = str(val) if val is not None else ""
            break
        elif hasattr(item, p_key):
            val = getattr(item, p_key)
            if callable(val):
                try: val = val()
                except Exception: pass
            prompt = str(val) if val is not None else ""
            break

    return str(episode_id), prompt

def generate_route_predictions(inputs: Any, tier: str) -> List[Dict[str, str]]:
    results = []
    items = _extract_items(inputs)

    for idx, item in enumerate(items):
        episode_id, prompt = _extract_id_and_prompt(item, idx)
        model_id = select_model_by_tier(prompt, tier)
        results.append({
            "episode_id": episode_id,
            "model_id": model_id
        })

    return results