"""
utils/charts.py
All Plotly visualizations for the Career Intelligence App.
"""

import plotly.graph_objects as go
import plotly.express       as px
import pandas               as pd


# ─── 1. Score Gauge ────────────────────────────────────────────────────────────
def plot_score_gauge(score: float) -> go.Figure:
    """Animated gauge chart for job fit score."""
    if   score >= 80: color = "#10B981"   # green
    elif score >= 60: color = "#F59E0B"   # amber
    elif score >= 40: color = "#FB923C"   # orange
    else:             color = "#EF4444"   # red

    interpretation = (
        "Excellent! Highly competitive 🚀" if score >= 80 else
        "Good fit – a bit of upskilling helps 💪" if score >= 60 else
        "Moderate – focus on key gaps 📚" if score >= 40 else
        "Significant upskilling needed 🎯"
    )

    fig = go.Figure(go.Indicator(
        mode  = "gauge+number+delta",
        value = score,
        delta = {"reference": 70, "valueformat": ".1f"},
        title = {"text": f"<b>{interpretation}</b>", "font": {"size": 14}},
        gauge = {
            "axis":  {"range": [0, 100], "tickwidth": 1},
            "bar":   {"color": color, "thickness": 0.25},
            "steps": [
                {"range": [0,  40], "color": "#FEE2E2"},
                {"range": [40, 60], "color": "#FEF3C7"},
                {"range": [60, 80], "color": "#D1FAE5"},
                {"range": [80, 100], "color": "#A7F3D0"},
            ],
            "threshold": {
                "line":  {"color": "#1F2937", "width": 4},
                "thickness": 0.75,
                "value": 70,
            },
        },
        number = {"suffix": "%", "font": {"size": 40}},
    ))

    fig.update_layout(
        height = 300,
        margin = dict(t=60, b=10, l=20, r=20),
        paper_bgcolor = "rgba(0,0,0,0)",
    )
    return fig


# ─── 2. Skill Radar Chart ──────────────────────────────────────────────────────
def plot_skill_radar(user_skills: dict, role: str, job_roles: dict) -> go.Figure:
    """Spider chart comparing user skills against role requirements."""
    level_map = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
    requirements = job_roles.get(role, {}).get("required_skills", {})

    common_skills = [s for s in requirements if s.lower() in {k.lower() for k in user_skills}]
    if not common_skills:
        common_skills = list(requirements.keys())[:6]

    user_values  = []
    req_values   = []

    for skill in common_skills:
        user_level = next(
            (v for k, v in user_skills.items() if k.lower() == skill.lower()), "beginner"
        )
        user_values.append(level_map.get(user_level.lower(), 1))
        req_min = requirements[skill].get("min_level", "intermediate")
        req_values.append(level_map.get(req_min.lower(), 2))

    categories = common_skills + [common_skills[0]]
    user_values  = user_values  + [user_values[0]]
    req_values   = req_values   + [req_values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=req_values, theta=categories,
        fill="toself", name="Required",
        line=dict(color="#EF4444", width=2),
        fillcolor="rgba(239,68,68,0.1)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=user_values, theta=categories,
        fill="toself", name="Your Level",
        line=dict(color="#4F46E5", width=2),
        fillcolor="rgba(79,70,229,0.2)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, 4],
                tickvals=[1,2,3,4],
                ticktext=["Beginner","Intermediate","Advanced","Expert"],
                tickfont=dict(size=9),
            )
        ),
        showlegend=True,
        height=320,
        margin=dict(t=40, b=40, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    return fig


# ─── 3. Salary Bar Chart ──────────────────────────────────────────────────────
def plot_salary_bar(salary: dict, role: str, location: str) -> go.Figure:
    """Bar chart comparing salary across experience levels."""
    exp_labels = ["Fresher", "1-2 Years", "3-5 Years", "5+ Years"]

    loc_display = location.split("–")[0].strip() if "–" in location else location

    # Approximate midpoints for visualization (INR, not exact)
    role_midpoints = {
        "Data Analyst":                [375000,  550000, 975000,  1600000],
        "Software Engineer":           [550000,  800000, 1500000, 2650000],
        "Product Manager":             [800000, 1250000, 2250000, 3750000],
        "Data Scientist":              [650000, 1050000, 1900000, 3000000],
        "Business Analyst":            [450000,  675000, 1150000, 1950000],
        "Digital Marketing Specialist":[325000,  500000, 850000,  1400000],
    }

    midpoints = role_midpoints.get(role, [350000, 550000, 1000000, 1700000])
    your_val  = salary["min"] + (salary["max"] - salary["min"]) * 0.5

    colors = ["#CBD5E1"] * 4
    # Highlight the user's experience level bar
    bar_colors = ["#4F46E5" if i == 0 else "#CBD5E1" for i in range(4)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=exp_labels,
        y=[m / 100000 for m in midpoints],
        marker_color=bar_colors,
        name="Market Average",
        text=[f"₹{m/100000:.1f}L" for m in midpoints],
        textposition="outside",
    ))

    fig.add_hline(
        y=your_val / 100000,
        line_dash="dot",
        line_color="#EF4444",
        line_width=2,
        annotation_text=f"Your Est: ₹{your_val/100000:.1f}L",
        annotation_position="right",
    )

    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Salary (Lakhs ₹)",
        height=300,
        margin=dict(t=30, b=30, l=30, r=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#F1F5F9"),
        showlegend=False,
    )
    return fig


# ─── 4. Skill Gap Chart ────────────────────────────────────────────────────────
def plot_skill_gap_chart(gaps: list) -> go.Figure:
    """Horizontal bar chart showing skill gaps by importance."""
    if not gaps:
        fig = go.Figure()
        fig.add_annotation(text="✅ No Critical Skill Gaps!", showarrow=False,
                           font=dict(size=18, color="#10B981"),
                           xref="paper", yref="paper", x=0.5, y=0.5)
        fig.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)")
        return fig

    level_map    = {"None": 0, "Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
    skills       = [g["skill"]         for g in gaps[:8]]
    current_vals = [level_map.get(g["current_level"],  0) for g in gaps[:8]]
    required_vals= [level_map.get(g["required_level"], 2) for g in gaps[:8]]
    priorities   = [g["priority"] for g in gaps[:8]]

    colors = ["#EF4444" if p == "High" else "#F59E0B" for p in priorities]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=skills, x=current_vals,
        orientation="h",
        name="Your Level",
        marker_color="#4F46E5",
        opacity=0.7,
    ))

    fig.add_trace(go.Bar(
        y=skills,
        x=[r - c for r, c in zip(required_vals, current_vals)],
        orientation="h",
        name="Gap to Fill",
        marker_color=colors,
        opacity=0.5,
        base=current_vals,
    ))

    fig.update_layout(
        barmode="overlay",
        xaxis=dict(
            tickvals=[0,1,2,3,4],
            ticktext=["None","Beginner","Intermediate","Advanced","Expert"],
            tickfont=dict(size=9),
        ),
        height=max(250, 50 * len(gaps[:8])),
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        xaxis_gridcolor="#F1F5F9",
    )
    return fig


# ─── 5. Timeline Chart ────────────────────────────────────────────────────────
def plot_timeline(milestones: list) -> go.Figure:
    """Horizontal timeline for career milestones."""
    months = [m["month"] for m in milestones]
    goals  = [m["goal"]  for m in milestones]
    labels = [f"Month {m}" for m in months]

    colors = px.colors.qualitative.Set2[:len(milestones)]

    fig = go.Figure()

    # Draw connecting line
    fig.add_trace(go.Scatter(
        x=months, y=[1]*len(months),
        mode="lines",
        line=dict(color="#CBD5E1", width=3),
        showlegend=False,
    ))

    # Draw milestone dots
    fig.add_trace(go.Scatter(
        x=months, y=[1]*len(months),
        mode="markers+text",
        marker=dict(size=18, color=colors, line=dict(width=2, color="white")),
        text=labels,
        textposition="top center",
        hovertext=goals,
        hoverinfo="text",
        showlegend=False,
    ))

    # Add goal annotations
    for i, (month, goal) in enumerate(zip(months, goals)):
        fig.add_annotation(
            x=month, y=0.75,
            text=f"<b>{goal[:45]}{'...' if len(goal)>45 else ''}</b>",
            showarrow=True, arrowhead=2,
            ax=0, ay=-30,
            font=dict(size=10),
            bgcolor="white",
            bordercolor=colors[i % len(colors)],
            borderwidth=1,
        )

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, max(months)+0.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.4, 1.3]),
        height=220,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
