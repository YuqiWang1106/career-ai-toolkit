# core/services/role_weighted_placement.py
import numpy as np

# === Grade scale ===
GRADE_SCALE = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "F": 0.0
}

# === Default thresholds ===
DEFAULT_THRESHOLDS = {
    "Tier1": {"fit": 0.85},
    "Tier2": {"fit": 0.65},
    "Tier3": {"fit": 0.45},
}

def normalize_scores(scores_dict):
    """Normalize skill scores to the 0–1 interval."""
    if not scores_dict:
        return {}
    return {k: min(max(v / 100.0, 0.0), 1.0) for k, v in scores_dict.items()}

def compute_skill_alignment(user_scores, weights):
    """Compute weighted skill alignment."""
    if not user_scores or not weights:
        return 0.0
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    score = sum(user_scores.get(k, 0.0) * weights[k] for k in weights)
    return round(score / total_weight, 3)

def classify_for_job(grades, job_weights, user_vals, thresholds):
    """
    Determine the tier based on course performance and skill alignment.
    Returns (tier_name, metrics_dict).
    """
    # === (1) Grade analysis ===
    core_grades = [GRADE_SCALE.get(g.get("grade"), 0) for g in grades if "CS" in g.get("code", "")]
    core_avg = np.mean(core_grades) if core_grades else 0
    fail_cnt = sum(1 for g in grades if g.get("grade") == "F")
    adv_cnt = sum(1 for g in grades if "Advanced" in g.get("title", ""))

    # === (2) Skill alignment ===
    hard_match = compute_skill_alignment(user_vals["hardskills"], job_weights["hardskills"])
    soft_match = compute_skill_alignment(user_vals["softskills"], job_weights["softskills"])

    # === (3) Course relevance ===
    course_rel = min(1.0, (core_avg / 4.0))
    hard_coverage = np.mean(list(user_vals["hardskills"].values()) or [0])
    key_coverage = np.mean(list(user_vals["softskills"].values()) or [0])

    # === (4) Composite metrics ===
    fit = round(0.5 * hard_match + 0.25 * soft_match + 0.25 * course_rel, 3)
    metrics = {
        "coreAvg": round(core_avg, 2),
        "failCnt": fail_cnt,
        "advCount": adv_cnt,
        "hardMatch": hard_match,
        "softMatch": soft_match,
        "hardCoverage": hard_coverage,
        "keyCoverage": key_coverage,
        "courseRel": course_rel,
        "fit": fit,
    }

    # === (5) Tier classification ===
    if fit >= thresholds["Tier1"]["fit"]:
        tier = "Tier1"
    elif fit >= thresholds["Tier2"]["fit"]:
        tier = "Tier2"
    else:
        tier = "Tier3"

    return tier, metrics
