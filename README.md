# Career AI Toolkit

How closely do a student’s skills match a target role, and what could they work on next? This toolkit contains three modules I wrote for the Career AI team project and adapted for standalone use. Two modules run locally. A third can turn a user’s own notes into a draft résumé entry.

## Try the offline example

The demo uses invented grades, skill scores, and role requirements. It requires Python 3.10 or later and NumPy.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python demo.py
python -m unittest discover -s tests -v
```

For the sample second-year student, the program prints a hard-skill match of 0.733, a soft-skill match of 0.700, and a course score of 1.000. The weighted result is 0.791. This selects Tier 2 and puts activities first, including a small hackathon or peer project. You can change the inputs and rerun the [demo](demo.py).

## How the recommendations work

1. The skill matcher normalizes self-reported scores and compares them with weights supplied for a role. It computes the overall score from hard skills (50%), soft skills (25%), and grades in courses whose code contains `CS` (25%). [Scoring code](career_ai/role_weighted_placement.py)
2. The recommendation rules use the resulting tier and academic year to choose courses, activities, and internship preparation. A first-year student sees courses and activities. For a third-year student, internship preparation comes first. [Recommendation rules](career_ai/recommend_by_tier_and_year.py)

The weights and thresholds are illustrative. The score has not been validated as a predictor of hiring or job performance.

## Optional AI résumé drafting

Install the optional dependencies with `python -m pip install -r requirements-ai.txt` and set `OPENAI_API_KEY` to call the résumé generator. Calling it sends the supplied activity, work summary, and optional fields to the configured OpenAI service. The offline demo and tests require no key.

The function takes its title, role, organization, and dates directly from the inputs. It asks the model to draft bullet points from the work summary and checks the structure of the response. Review the wording against your records before using it. The tests use a simulated response to check the request, formatting, and handling of invalid output. [Résumé generator](career_ai/resume_entry_generator.py) · [Offline tests](tests/test_resume_entry.py)
