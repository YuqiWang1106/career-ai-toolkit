"""New offline demonstration using invented inputs; no user data is loaded."""

import json

from career_ai.recommend_by_tier_and_year import recommend_by_tier_and_year
from career_ai.role_weighted_placement import classify_for_job, normalize_scores


def main():
    # Invented scores and weights, chosen solely to illustrate the calculation.
    user = {
        "hardskills": normalize_scores({"Python": 80, "SQL": 60}),
        "softskills": normalize_scores({"Communication": 70}),
    }
    weights = {
        "hardskills": {"Python": 2, "SQL": 1},
        "softskills": {"Communication": 1},
    }
    grades = [{"code": "CS101", "title": "Introductory Computing", "grade": "A"}]
    thresholds = {"Tier1": {"fit": 0.85}, "Tier2": {"fit": 0.65}}
    tier, metrics = classify_for_job(grades, weights, user, thresholds)
    result = {"tier": tier, "metrics": metrics, "suggestions": recommend_by_tier_and_year(tier, 2)}
    print(json.dumps(result, indent=2, default=float))


if __name__ == "__main__":
    main()
