"""
╔══════════════════════════════════════════════════════════════╗
║         CAREER INTELLIGENCE APP - Python Edition             ║
║         Built with Streamlit for Data Science Portfolio      ║
╚══════════════════════════════════════════════════════════════╝

A complete AI-powered career analysis tool for the Indian job market.
Built 100% in Python using Streamlit, Pandas, Plotly, and more.

Author: Manish kumar
Version: 2.0.0
"""

import streamlit as st

# ─── Page Configuration (MUST be first Streamlit command) ─────────────────────
st.set_page_config(
    page_title="Career Intelligence India",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Career Intelligence App - Built 100% in Python for Indian Job Market"
    }
)

# ─── Imports ──────────────────────────────────────────────────────────────────
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from algorithms.scoring      import calculate_job_fit, analyze_strengths, identify_skill_gaps
from algorithms.salary       import estimate_salary
from algorithms.recommender  import generate_recommendations
from data.database           import JOB_ROLES, SALARY_DATA, SKILLS_DB
from utils.styling           import apply_custom_css
from utils.charts            import (
    plot_score_gauge,
    plot_skill_radar,
    plot_salary_bar,
    plot_skill_gap_chart,
    plot_timeline
)

# ─── Apply Custom CSS ─────────────────────────────────────────────────────────
apply_custom_css()

# ─── Session State Initialization ─────────────────────────────────────────────
if "skills"          not in st.session_state: st.session_state.skills    = [{"name": "", "level": "Beginner"}]
if "analyzed"        not in st.session_state: st.session_state.analyzed  = False
if "results"         not in st.session_state: st.session_state.results   = None
if "profile"         not in st.session_state: st.session_state.profile   = {}

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Career Intelligence")
    st.markdown("*AI-Powered Career Analysis for India*")
    st.markdown("---")

    st.markdown("### 📋 Navigation")
    st.markdown("- 🏠 **Home** – Analyze Profile")
    st.markdown("- 📊 Results appear below")
    st.markdown("- 💾 Download PDF report")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool analyzes your career profile
    against **real Indian job market data**
    and gives you:

    ✅ Job Fit Score  
    ✅ Salary Estimate (INR)  
    ✅ Skill Gap Analysis  
    ✅ Learning Roadmap  
    ✅ Visual Insights  
    """)

    st.markdown("---")
    st.markdown("### 📌 Supported Roles")
    for role in JOB_ROLES.keys():
        st.markdown(f"- {role}")

    st.markdown("---")
    st.caption("⚠️ Predictions are estimates based on market trends. Not guaranteed.")
    st.caption("v2.0.0 | Made for Indian Job Seekers 🇮🇳")

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("# 🎯 Career Intelligence Platform")
    st.markdown("#### AI-Powered Career Analysis for the Indian Job Market")
with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🇮🇳 India-Specific Data")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.analyzed:
    st.markdown("## 📝 Enter Your Profile")
    st.markdown("Fill in your details below to get your personalized career analysis.")

    with st.form("career_form"):
        # ── Row 1: Role + Experience ────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎯 Target Job Role")
            role = st.selectbox(
                "Select the role you want to work in:",
                options=list(JOB_ROLES.keys()),
                help="Choose the job role you are targeting"
            )
        with col2:
            st.markdown("### 💼 Work Experience")
            experience = st.selectbox(
                "How many years of experience do you have?",
                options=["Fresher (0 years)", "1-2 years", "3-5 years", "5+ years"],
                help="Select your total professional experience"
            )

        # ── Row 2: Education + Location ─────────────────────────────────────
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### 🎓 Education Level")
            education = st.selectbox(
                "Highest qualification:",
                options=["Diploma / Certificate", "Bachelor's Degree", "Master's Degree", "PhD"],
                index=1,
                help="Select your highest education level"
            )
        with col4:
            st.markdown("### 📍 Target Location")
            location = st.selectbox(
                "Where do you want to work?",
                options=[
                    "Tier 1 – Mumbai, Delhi, Bangalore, Hyderabad, Pune",
                    "Tier 2 – Ahmedabad, Jaipur, Kochi, Chandigarh",
                    "Tier 3 – Small cities & towns",
                    "Remote / Work from Home"
                ],
                help="Location affects salary estimates significantly"
            )

        # ── Skills Section ───────────────────────────────────────────────────
        st.markdown("### 🛠️ Your Skills & Proficiency")
        st.markdown("Add all your relevant skills and rate your proficiency honestly.")

        skill_cols = st.columns([3, 2])
        with skill_cols[0]:
            st.markdown("**Skill Name**")
        with skill_cols[1]:
            st.markdown("**Proficiency Level**")

        # Dynamic skill inputs (up to 12)
        skills_data = {}
        for i in range(12):
            c1, c2 = st.columns([3, 2])
            with c1:
                skill_name = st.text_input(
                    f"Skill {i+1}",
                    placeholder=f"e.g., {'Python' if i==0 else 'SQL' if i==1 else 'Excel' if i==2 else 'Skill name...'}",
                    key=f"skill_name_{i}",
                    label_visibility="collapsed"
                )
            with c2:
                skill_level = st.selectbox(
                    f"Level {i+1}",
                    options=["Beginner", "Intermediate", "Advanced", "Expert"],
                    key=f"skill_level_{i}",
                    label_visibility="collapsed"
                )
            if skill_name.strip():
                skills_data[skill_name.strip()] = skill_level

        # ── Submit Button ───────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🔍 Analyze My Career Profile",
            use_container_width=True,
            type="primary"
        )

    # ── Form Processing ──────────────────────────────────────────────────────
    if submitted:
        if not skills_data:
            st.error("❌ Please add at least one skill before analyzing!")
        else:
            # Map display values to internal codes
            exp_map = {
                "Fresher (0 years)": "fresher",
                "1-2 years": "1-2",
                "3-5 years": "3-5",
                "5+ years": "5+"
            }
            edu_map = {
                "Diploma / Certificate": "diploma",
                "Bachelor's Degree": "bachelors",
                "Master's Degree": "masters",
                "PhD": "phd"
            }
            loc_map = {
                "Tier 1 – Mumbai, Delhi, Bangalore, Hyderabad, Pune": "tier1",
                "Tier 2 – Ahmedabad, Jaipur, Kochi, Chandigarh": "tier2",
                "Tier 3 – Small cities & towns": "tier3",
                "Remote / Work from Home": "remote"
            }

            exp_code = exp_map[experience]
            edu_code = edu_map[education]
            loc_code = loc_map[location]

            # Run analysis with a progress bar
            with st.spinner("🔍 Analyzing your profile against Indian job market data..."):
                import time
                progress = st.progress(0, text="Loading market data...")
                time.sleep(0.3)
                progress.progress(20, text="Calculating job fit score...")

                fit_score = calculate_job_fit(role, skills_data, exp_code, edu_code, JOB_ROLES)
                progress.progress(40, text="Analyzing your strengths...")

                strengths = analyze_strengths(role, skills_data, JOB_ROLES)
                progress.progress(60, text="Identifying skill gaps...")

                gaps = identify_skill_gaps(role, skills_data, JOB_ROLES)
                progress.progress(75, text="Estimating salary range...")

                salary = estimate_salary(role, loc_code, exp_code, fit_score, SALARY_DATA)
                progress.progress(90, text="Generating recommendations...")

                recommendations = generate_recommendations(role, skills_data, gaps, exp_code, JOB_ROLES, SKILLS_DB)
                progress.progress(100, text="Done!")
                time.sleep(0.3)
                progress.empty()

            # Save to session state
            st.session_state.results = {
                "fit_score":       fit_score,
                "strengths":       strengths,
                "gaps":            gaps,
                "salary":          salary,
                "recommendations": recommendations
            }
            st.session_state.profile = {
                "role":       role,
                "experience": experience,
                "education":  education,
                "location":   location,
                "skills":     skills_data
            }
            st.session_state.analyzed = True
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.analyzed and st.session_state.results:
    results = st.session_state.results
    profile = st.session_state.profile

    # ── Re-analyze Button ────────────────────────────────────────────────────
    if st.button("🔄 Analyze Another Profile", type="secondary"):
        st.session_state.analyzed = False
        st.session_state.results  = None
        st.session_state.profile  = {}
        st.rerun()

    st.markdown(f"## 📊 Career Analysis Results")
    st.markdown(f"**Role:** {profile['role']} &nbsp;|&nbsp; **Experience:** {profile['experience']} &nbsp;|&nbsp; **Location:** {profile['location']}")
    st.markdown("---")

    # ════════════════════════════════
    #  ROW 1: Score + Salary KPIs
    # ════════════════════════════════
    k1, k2, k3, k4 = st.columns(4)

    score = results["fit_score"]
    salary = results["salary"]

    with k1:
        st.metric(
            label="🎯 Job Fit Score",
            value=f"{score:.1f}%",
            delta="Strong" if score >= 70 else "Needs Work"
        )
    with k2:
        st.metric(
            label="💰 Min Salary (Annual)",
            value=salary["formatted_min"],
            delta="INR"
        )
    with k3:
        st.metric(
            label="💰 Max Salary (Annual)",
            value=salary["formatted_max"],
            delta="INR"
        )
    with k4:
        st.metric(
            label="📋 Skill Gaps Found",
            value=len(results["gaps"]),
            delta="High Priority" if any(g["priority"] == "High" for g in results["gaps"]) else "Manageable"
        )

    st.markdown("---")

    # ════════════════════════════════
    #  ROW 2: Score Gauge + Radar Chart
    # ════════════════════════════════
    st.markdown("### 📈 Visual Analysis")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### 🎯 Job Fit Score")
        gauge_fig = plot_score_gauge(score)
        st.plotly_chart(gauge_fig, use_container_width=True)

    with chart_col2:
        st.markdown("#### 🕸️ Skills vs Requirements Radar")
        radar_fig = plot_skill_radar(profile["skills"], profile["role"], JOB_ROLES)
        st.plotly_chart(radar_fig, use_container_width=True)

    # ════════════════════════════════
    #  ROW 3: Salary + Gap Charts
    # ════════════════════════════════
    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.markdown("#### 💰 Salary Range Comparison")
        salary_fig = plot_salary_bar(salary, profile["role"], profile["location"])
        st.plotly_chart(salary_fig, use_container_width=True)

    with chart_col4:
        st.markdown("#### ⚠️ Skill Gap Analysis")
        gap_fig = plot_skill_gap_chart(results["gaps"])
        st.plotly_chart(gap_fig, use_container_width=True)

    st.markdown("---")

    # ════════════════════════════════
    #  ROW 4: Strengths & Gaps
    # ════════════════════════════════
    st.markdown("### 💪 Strengths & Skill Gaps")
    str_col, gap_col = st.columns(2)

    with str_col:
        st.markdown("#### ✅ Your Key Strengths")
        if results["strengths"]:
            for s in results["strengths"]:
                with st.container():
                    st.success(f"**{s['skill']}** — {s['your_level']}")
                    st.caption(f"🏷️ {s['importance']} | {s['note']}")
        else:
            st.warning("No major strengths identified for this role yet. Keep learning!")

    with gap_col:
        st.markdown("#### ⚠️ Skill Gaps to Address")
        if results["gaps"]:
            for g in results["gaps"]:
                color = st.error if g["priority"] == "High" else st.warning
                color(f"**{g['skill']}** — {g['current_level']} → {g['required_level']}")
                st.caption(f"🏷️ {g['priority']} Priority | {g['note']}")
        else:
            st.success("🎉 No critical skill gaps! You're well prepared.")

    st.markdown("---")

    # ════════════════════════════════
    #  ROW 5: Recommendations
    # ════════════════════════════════
    st.markdown("### 🚀 Personalized Recommendations")
    recs = results["recommendations"]

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Immediate Priorities",
        "📚 Learning Resources",
        "📅 Timeline & Milestones",
        "💼 Job Search Tips"
    ])

    with tab1:
        st.markdown("#### Top Actions to Take Right Now")
        if recs.get("immediate_priorities"):
            for i, p in enumerate(recs["immediate_priorities"], 1):
                with st.expander(f"Priority {i}: {p['action']}", expanded=(i == 1)):
                    st.markdown(f"**Why:** {p['reason']}")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.info(f"🎯 Target Level: **{p['target']}**")
                    with col_b:
                        st.info(f"⏱️ Est. Time: **{p['estimated_time']}**")
        else:
            st.success("You're already well-prepared for this role!")

    with tab2:
        st.markdown("#### Curated Learning Resources for Your Skill Gaps")
        if recs.get("learning_resources"):
            for res in recs["learning_resources"]:
                with st.expander(f"📖 {res['skill']} — {res['priority']} Priority"):
                    st.markdown(f"**Practice Tip:** {res['practice_tips']}")
                    if res.get("resources"):
                        st.markdown("**Recommended Resources:**")
                        df = pd.DataFrame(res["resources"])
                        if not df.empty and all(c in df.columns for c in ["name","type","cost","duration"]):
                            st.dataframe(
                                df[["name", "type", "cost", "duration"]],
                                use_container_width=True,
                                hide_index=True
                            )
        else:
            st.info("No specific resources needed – you're on track!")

    with tab3:
        st.markdown("#### Your Roadmap to Getting Hired")
        timeline = recs.get("timeline", {})
        if timeline:
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.success(f"✅ **Job-Ready In:** {timeline.get('ready_for_jobs', 'N/A')}")
            with t_col2:
                st.info(f"🏆 **Competitive Profile In:** {timeline.get('competitive_profile', 'N/A')}")

            if timeline.get("milestones"):
                st.markdown("**📍 Milestones:**")
                timeline_fig = plot_timeline(timeline["milestones"])
                st.plotly_chart(timeline_fig, use_container_width=True)

    with tab4:
        st.markdown("#### Smart Job Search Strategies")
        tips = recs.get("job_search_tips", [])
        if tips:
            for i, tip in enumerate(tips, 1):
                st.markdown(f"**{i}.** ✓ {tip}")

        st.markdown("---")
        st.markdown("**🔗 Recommended Job Portals:**")
        portal_col1, portal_col2, portal_col3 = st.columns(3)
        with portal_col1:
            st.markdown("- [Naukri.com](https://naukri.com)\n- [LinkedIn Jobs](https://linkedin.com/jobs)")
        with portal_col2:
            st.markdown("- [Internshala](https://internshala.com)\n- [AngelList](https://angel.co)")
        with portal_col3:
            st.markdown("- [Glassdoor](https://glassdoor.co.in)\n- [Indeed India](https://indeed.co.in)")

        if recs.get("certifications"):
            st.markdown("---")
            st.markdown("**🎓 Recommended Certifications:**")
            cert_df = pd.DataFrame(recs["certifications"])
            st.dataframe(cert_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ════════════════════════════════
    #  ROW 6: Skills Summary Table
    # ════════════════════════════════
    st.markdown("### 📋 Your Complete Skills Summary")
    if profile["skills"]:
        skill_rows = []
        role_reqs  = JOB_ROLES.get(profile["role"], {}).get("required_skills", {})
        for skill, level in profile["skills"].items():
            req = role_reqs.get(skill, {})
            importance = req.get("importance", 0)
            importance_label = (
                "🔴 Critical"   if importance > 0.8 else
                "🟡 Important"  if importance > 0.5 else
                "🟢 Bonus"      if importance > 0    else
                "⚪ Not in Role"
            )
            skill_rows.append({
                "Skill":       skill,
                "Your Level":  level,
                "Role Need":   importance_label,
                "Min Required": req.get("min_level", "N/A").capitalize()
            })

        skill_df = pd.DataFrame(skill_rows)
        st.dataframe(skill_df, use_container_width=True, hide_index=True)

    # ════════════════════════════════
    #  DISCLAIMER
    # ════════════════════════════════
    st.markdown("---")
    st.caption("""
    ⚠️ **Disclaimer:** All predictions are estimates based on general Indian job market trends (2024-2025).
    Actual salaries, hiring decisions, and career outcomes vary based on company, industry, economic conditions,
    and individual performance. This tool is for guidance only and does not guarantee employment or specific salary.
    """)
