"""
algorithms/scoring.py
Job fit score calculation, strength analysis, and skill gap identification.
"""

def get_proficiency_weight(level: str) -> float:
    """Convert proficiency level to a 0-1 numerical weight."""
    return {"expert": 1.0, "advanced": 0.75, "intermediate": 0.5, "beginner": 0.25}.get(level.lower(), 0.25)


def calculate_job_fit(role, user_skills, experience, education, job_roles) -> float:
    """
    Calculate overall job fit score (0–100).

    Formula:
        skill_score  = Σ(proficiency_weight × importance × 100) / total_importance
        final_score  = skill_score + experience_bonus + education_bonus  (capped at 100)
    """
    if role not in job_roles:
        return 0.0

    requirements  = job_roles[role]["required_skills"]
    user_lower    = {k.lower(): v for k, v in user_skills.items()}

    skill_score   = 0.0
    total_weight  = 0.0

    for skill, req in requirements.items():
        importance = req["importance"]
        total_weight += importance

        if skill.lower() in user_lower:
            pw           = get_proficiency_weight(user_lower[skill.lower()])
            skill_score += pw * importance * 100

    base_score = (skill_score / total_weight) if total_weight > 0 else 0.0

    exp_bonus  = {"fresher": 0, "1-2": 5, "3-5": 10, "5+": 15}.get(experience, 0)
    edu_bonus  = {"phd": 10, "masters": 5, "bachelors": 0, "diploma": -5}.get(education.lower(), 0)

    return max(0.0, min(100.0, base_score + exp_bonus + edu_bonus))


def analyze_strengths(role, user_skills, job_roles) -> list:
    """Return list of skills where the user is strong AND the skill matters."""
    if role not in job_roles:
        return []

    requirements = job_roles[role]["required_skills"]
    user_lower   = {k.lower(): v for k, v in user_skills.items()}
    strengths    = []

    for skill, req in requirements.items():
        if skill.lower() in user_lower:
            level      = user_lower[skill.lower()]
            pw         = get_proficiency_weight(level)
            importance = req["importance"]

            if pw >= 0.5 and importance >= 0.5:
                strengths.append({
                    "skill":      skill,
                    "your_level": level.capitalize(),
                    "importance": "Critical" if importance > 0.8 else "Important",
                    "note":       req.get("note", f"Strong {skill} is valuable for this role"),
                })

    return sorted(strengths, key=lambda x: 0 if x["importance"] == "Critical" else 1)


def identify_skill_gaps(role, user_skills, job_roles) -> list:
    """Return list of missing or under-developed skills."""
    if role not in job_roles:
        return []

    requirements = job_roles[role]["required_skills"]
    user_lower   = {k.lower(): v for k, v in user_skills.items()}
    gaps         = []

    for skill, req in requirements.items():
        importance = req["importance"]
        min_level  = req.get("min_level", "intermediate")

        if importance < 0.6:
            continue  # Skip low-importance skills

        if skill.lower() not in user_lower:
            gaps.append({
                "skill":         skill,
                "current_level": "None",
                "required_level": min_level.capitalize(),
                "priority":      "High" if importance > 0.8 else "Medium",
                "note":          req.get("note", f"{skill} is required for this role"),
                "importance":    importance,
            })
        else:
            user_pw = get_proficiency_weight(user_lower[skill.lower()])
            req_pw  = get_proficiency_weight(min_level)
            if user_pw < req_pw:
                gaps.append({
                    "skill":         skill,
                    "current_level": user_lower[skill.lower()].capitalize(),
                    "required_level": min_level.capitalize(),
                    "priority":      "High" if importance > 0.8 else "Medium",
                    "note":          f"Improve {skill} from {user_lower[skill.lower()]} to {min_level}",
                    "importance":    importance,
                })

    order = {"High": 0, "Medium": 1}
    return sorted(gaps, key=lambda x: order.get(x["priority"], 2))
