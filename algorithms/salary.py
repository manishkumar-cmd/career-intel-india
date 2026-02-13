"""
algorithms/salary.py
Salary estimation based on Indian market data.
"""

def format_inr(amount: float) -> str:
    """Format amount in Indian number system (Lakhs / Crores)."""
    amount = int(amount)
    if amount >= 10_000_000:
        return f"₹{amount/10_000_000:.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount/100_000:.2f} L"
    else:
        return f"₹{amount/1000:.0f}K"


def estimate_salary(role, location, experience, fit_score, salary_data) -> dict:
    """
    Estimate salary range in INR.

    Uses pre-computed range data from SALARY_DATA, then applies a
    skill-fit bonus of up to ±15 % inside the range.
    """
    if role not in salary_data:
        base_min, base_max = 250000, 400000
    else:
        ranges   = salary_data[role]["ranges"]
        exp_data = ranges.get(experience, ranges["fresher"])
        loc_key  = location if location in exp_data else "tier3"
        base_min, base_max = exp_data[loc_key]

    # Skill fit adjustment within range (high fit → upper end, low fit → lower end)
    fit_ratio  = fit_score / 100
    estimated  = base_min + (base_max - base_min) * fit_ratio

    # ±10 % variance band
    final_min  = round(estimated * 0.90 / 10000) * 10000
    final_max  = round(estimated * 1.10 / 10000) * 10000

    # Keep within absolute range
    final_min  = max(final_min, base_min)
    final_max  = min(final_max, base_max)

    return {
        "min":           int(final_min),
        "max":           int(final_max),
        "formatted_min": format_inr(final_min),
        "formatted_max": format_inr(final_max),
        "annual_range":  f"{format_inr(final_min)} – {format_inr(final_max)} per annum",
        "monthly_range": f"{format_inr(final_min/12)} – {format_inr(final_max/12)} per month",
        "base_min":      int(base_min),
        "base_max":      int(base_max),
        "note": _salary_note(experience, fit_score, location),
    }


def _salary_note(experience, fit_score, location) -> str:
    notes = []
    if experience == "fresher":
        notes.append("As a fresher, focus on building skills and portfolio projects.")
    if fit_score < 50:
        notes.append("Upskilling in key areas will directly increase your earning potential.")
    if fit_score >= 80:
        notes.append("Your strong skill profile puts you at the upper end of the salary range.")
    if location in ("tier3", "remote"):
        notes.append("Tier-1 city roles typically offer 30-40% higher salaries.")
    notes.append("Salary varies by company size, funding stage, and industry sector.")
    return " ".join(notes)
