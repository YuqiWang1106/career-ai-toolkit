"""New offline tests for the selected original modules using invented inputs."""

import unittest

from career_ai.recommend_by_tier_and_year import recommend_by_tier_and_year
from career_ai.role_weighted_placement import (
    classify_for_job,
    compute_skill_alignment,
    normalize_scores,
)


class SkillAlignmentTests(unittest.TestCase):
    def test_normalization_clamps_input_to_unit_interval(self):
        self.assertEqual(normalize_scores({"a": -4, "b": 50, "c": 120}), {"a": 0, "b": 0.5, "c": 1})

    def test_weighted_alignment_counts_missing_skill_as_zero(self):
        self.assertEqual(compute_skill_alignment({"a": 0.9}, {"a": 2, "b": 1}), 0.6)
        self.assertEqual(compute_skill_alignment({"a": 0.9}, {"a": 0}), 0.0)

    def test_fit_calculation_and_threshold(self):
        user = {"hardskills": {"a": 0.8}, "softskills": {"b": 0.6}}
        weights = {"hardskills": {"a": 1}, "softskills": {"b": 1}}
        grades = [{"code": "CS101", "title": "Introductory Computing", "grade": "A"}]
        thresholds = {"Tier1": {"fit": 0.85}, "Tier2": {"fit": 0.65}}
        tier, metrics = classify_for_job(grades, weights, user, thresholds)
        self.assertEqual(metrics["fit"], 0.8)
        self.assertEqual(tier, "Tier2")

    def test_first_year_recommendation_omits_internships(self):
        result = recommend_by_tier_and_year("Tier2", 1)
        self.assertEqual(result["recommendations"]["internships"], [])
        self.assertTrue(result["recommendations"]["courses"])

    def test_later_year_adds_internship_suggestion(self):
        result = recommend_by_tier_and_year("Tier2", 3)
        self.assertIn("Apply for summer internships", result["recommendations"]["internships"])


if __name__ == "__main__":
    unittest.main()
