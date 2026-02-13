"""
algorithms/recommender.py
Personalized recommendations generator.
"""

def generate_recommendations(role, user_skills, skill_gaps, experience, job_roles, skills_db) -> dict:
    """Return a comprehensive recommendations dict."""
    return {
        "immediate_priorities": _priorities(skill_gaps),
        "learning_resources":   _resources(skill_gaps, skills_db),
        "timeline":             _timeline(skill_gaps, experience),
        "job_search_tips":      _job_tips(role, experience, len(skill_gaps)),
        "certifications":       job_roles.get(role, {}).get("certifications", []),
    }


def _priorities(skill_gaps) -> list:
    """Top 3 high-priority skills to work on immediately."""
    high = [g for g in skill_gaps if g["priority"] == "High"][:3]
    return [
        {
            "action":         f"Master {g['skill']}",
            "reason":         g["note"],
            "target":         g["required_level"],
            "estimated_time": _learn_time(g["current_level"], g["required_level"]),
        }
        for g in high
    ]


def _resources(skill_gaps, skills_db) -> list:
    out = []
    for gap in skill_gaps[:5]:
        skill = gap["skill"]
        if skill in skills_db:
            out.append({
                "skill":         skill,
                "priority":      gap["priority"],
                "resources":     skills_db[skill].get("resources", []),
                "practice_tips": skills_db[skill].get("practice_tips", ""),
            })
    return out


def _learn_time(current: str, target: str) -> str:
    order   = ["none", "beginner", "intermediate", "advanced", "expert"]
    c_idx   = order.index(current.lower()) if current.lower() in order else 0
    t_idx   = order.index(target.lower())  if target.lower()  in order else 2
    gap     = abs(t_idx - c_idx)
    times   = {1: "2-4 weeks", 2: "6-8 weeks", 3: "3-4 months", 4: "6-8 months"}
    return  times.get(gap, "4-8 weeks")


def _timeline(skill_gaps, experience) -> dict:
    n_critical = len([g for g in skill_gaps if g["priority"] == "High"])

    if experience == "fresher":
        if n_critical <= 2:
            return {
                "ready_for_jobs":      "3-4 months",
                "competitive_profile": "6-8 months",
                "milestones": [
                    {"month": 1, "goal": "Complete foundational learning in top-priority skills"},
                    {"month": 2, "goal": "Build 1-2 hands-on portfolio projects"},
                    {"month": 3, "goal": "Start applying to internships and entry-level roles"},
                    {"month": 6, "goal": "Competitive profile – actively interview for full-time roles"},
                ],
            }
        else:
            return {
                "ready_for_jobs":      "6-8 months",
                "competitive_profile": "10-12 months",
                "milestones": [
                    {"month": 1,  "goal": "Focus on most critical skill gaps (SQL, primary tool)"},
                    {"month": 3,  "goal": "Complete 2 substantial end-to-end projects"},
                    {"month": 6,  "goal": "Begin job applications, continue secondary upskilling"},
                    {"month": 10, "goal": "Strong portfolio, competitive for most positions"},
                ],
            }
    else:
        return {
            "ready_for_jobs":      "1-2 months",
            "competitive_profile": "3-4 months",
            "milestones": [
                {"month": 1, "goal": "Address critical skill gaps via targeted learning"},
                {"month": 2, "goal": "Update resume and portfolio with new skills"},
                {"month": 3, "goal": "Actively apply and attend interviews"},
            ],
        }


def _job_tips(role, experience, num_gaps) -> list:
    role_tips = {
        "Data Analyst": [
            "Highlight SQL and Excel prominently in your resume",
            "Create a GitHub portfolio with 2-3 data analysis projects",
            "Target companies: Analytics firms, BFSI, startups, e-commerce",
            "Search titles: Junior Data Analyst, MIS Executive, Associate Analyst",
        ],
        "Software Engineer": [
            "Practice DSA daily on LeetCode / HackerRank",
            "Build 3-5 full-stack projects showcasing different technologies",
            "Target: Product companies, startups, IT service firms",
            "Prepare system design answers for senior interviews",
        ],
        "Product Manager": [
            "Create case studies of product teardowns and strategy",
            "Network extensively with PMs on LinkedIn",
            "Target: Startups, fintech, edtech, e-commerce platforms",
            "Demonstrate data-driven + empathy-driven decision making",
        ],
        "Data Scientist": [
            "Compete on Kaggle to build credibility and skills",
            "Write articles on Medium / LinkedIn about your projects",
            "Target: Analytics firms, tech companies, research labs",
            "Showcase end-to-end ML projects with business impact",
        ],
    }

    tips = list(role_tips.get(role, [
        "Research companies hiring for this role in India",
        "Tailor your resume to highlight relevant skills",
        "Network with professionals in this field on LinkedIn",
    ]))

    if experience == "fresher":
        tips += [
            "Consider internships (3-6 months) as the best entry point",
            "Use Internshala and AngelList for startup opportunities",
            "Attend virtual career fairs and free webinars",
        ]

    if num_gaps > 3:
        tips.append("Upskill before mass applying – quality applications beat quantity")
    else:
        tips.append("Your profile is competitive – start applying actively now!")

    return tips[:8]
