# core/services/recommend_by_tier_and_year.py
"""
Rule-based Recommendation Generator
Generates recommended courses, activities, internships, and project focus areas
based on Tier (Tier1, Tier2, Tier3) and academic year (1–4).
"""

def recommend_by_tier_and_year(tier: str, year: int):
    """
    Build recommendations for the given tier and academic year.
    Returns a structure like:
    {
        "tier": "Tier2",
        "year": 3,
        "recommendations": {
            "courses": [...],
            "activities": [...],
            "internships": [...]
        }
    }
    """

    # === Generic template ===
    reco = {
        "tier": tier,
        "year": year,
        "recommendations": {
            "courses": [],
            "activities": [],
            "internships": [],
        },
        "category_importance": []  # Prioritized categories
    }

    # === Tier1: solid foundation, focus on depth ===
    if tier == "Tier1":
        reco["recommendations"]["courses"] = [
            "Advanced Algorithms",
            "Distributed Systems",
            "Cloud Computing",
            "Machine Learning Engineering",
        ]
        reco["recommendations"]["activities"] = [
            "Join competitive programming contests (ICPC, Codeforces)",
            "Contribute to open-source projects",
            "Research assistant positions with professors",
        ]
        reco["recommendations"]["internships"] = [
            "Apply for research-oriented or R&D internships",
            "Industry internships at top tech companies",
        ]
        reco["category_importance"] = ["internships", "activities", "courses"]


    # === Tier2: moderate skills, reinforce fundamentals + projects ===
    elif tier == "Tier2":
        reco["recommendations"]["courses"] = [
            "Operating Systems",
            "Database Systems",
            "Computer Networks",
            "Software Engineering Principles",
        ]
        reco["recommendations"]["activities"] = [
            "Participate in hackathons or innovation challenges",
            "Join school technical clubs or online bootcamps",
            "Build independent projects hosted on GitHub",
        ]
        reco["recommendations"]["internships"] = [
            "Summer internships or remote developer programs",
            "Applied research assistantships or data lab work",
        ]
        reco["category_importance"] = ["activities", "courses", "internships"]


    # === Tier3: early stage, focus on fundamentals and small projects ===
    elif tier == "Tier3":
        reco["recommendations"]["courses"] = [
            "Intro to Programming (Python, Java)",
            "Data Structures & Algorithms",
            "Discrete Math",
            "Intro to Web Development",
        ]
        reco["recommendations"]["activities"] = [
            "Join beginner coding workshops",
            "Online courses (Coursera, freeCodeCamp)",
            "Pair-programming sessions or student study groups",
        ]
        reco["recommendations"]["internships"] = [
            "Campus technical assistantships",
            "Online remote internships (entry-level)",
        ]
        reco["category_importance"] = ["courses", "activities", "internships"]


    if year == 1:
        # First-year students focus on learning and activities
        reco["recommendations"]["internships"] = []
        reco["category_importance"] = ["courses", "activities", "internships"]
    elif year == 2:
        reco["recommendations"]["activities"].append("Participate in small hackathons or peer projects")
        reco["category_importance"] = ["activities", "courses", "internships"]
    elif year == 3:
        reco["recommendations"]["internships"].append("Apply for summer internships")
        reco["category_importance"] = ["internships", "activities", "courses"]
    elif year == 4:
        reco["recommendations"]["internships"].append("Prepare for full-time job applications")
        reco["category_importance"] = ["internships", "courses", "activities"]

    return reco
