"""
data/database.py
All Indian job market data stored as Python dictionaries.
No external JSON files needed - everything in one place!
"""

# ══════════════════════════════════════════════════════════════════════════════
#  JOB ROLES DATABASE
# ══════════════════════════════════════════════════════════════════════════════
JOB_ROLES = {
    "Data Analyst": {
        "description": "Analyzes data to derive insights and support business decisions",
        "required_skills": {
            "SQL":           {"importance": 0.95, "min_level": "advanced",      "note": "Most critical skill – complex queries, JOINs, window functions"},
            "Excel":         {"importance": 0.85, "min_level": "advanced",      "note": "Pivot tables, VLOOKUP, macros, advanced charts"},
            "Python":        {"importance": 0.75, "min_level": "intermediate",  "note": "Pandas, NumPy, Matplotlib for data manipulation"},
            "Power BI":      {"importance": 0.80, "min_level": "intermediate",  "note": "Interactive dashboards, DAX formulas, data modeling"},
            "Statistics":    {"importance": 0.70, "min_level": "intermediate",  "note": "Hypothesis testing, regression, descriptive stats"},
            "Tableau":       {"importance": 0.65, "min_level": "beginner",      "note": "Alternative to Power BI – know at least one BI tool"},
            "Data Cleaning": {"importance": 0.75, "min_level": "intermediate",  "note": "Handle missing data, outliers, data transformation"},
        },
        "certifications": [
            {"name": "Google Data Analytics Certificate", "provider": "Coursera",   "cost": "₹3,000-5,000",   "duration": "6 months",    "value": "High"},
            {"name": "Microsoft PL-300 Power BI",         "provider": "Microsoft",  "cost": "₹4,000-6,000",   "duration": "3-4 months",  "value": "High"},
            {"name": "IBM Data Analyst Certificate",      "provider": "Coursera",   "cost": "₹3,000-5,000",   "duration": "4 months",    "value": "Medium"},
        ]
    },

    "Software Engineer": {
        "description": "Designs, develops, and maintains software applications",
        "required_skills": {
            "Data Structures & Algorithms": {"importance": 0.95, "min_level": "advanced",     "note": "Essential for all tech interviews in India"},
            "Programming Language":         {"importance": 0.90, "min_level": "advanced",     "note": "Java, Python, C++, JavaScript – master at least one"},
            "Database / SQL":               {"importance": 0.80, "min_level": "intermediate", "note": "MySQL, PostgreSQL, MongoDB"},
            "Git / Version Control":        {"importance": 0.85, "min_level": "intermediate", "note": "GitHub, branching, pull requests"},
            "Web Frameworks":               {"importance": 0.75, "min_level": "intermediate", "note": "Django, Spring Boot, Node.js, React"},
            "System Design":               {"importance": 0.70, "min_level": "beginner",     "note": "Scalable architecture (critical for senior roles)"},
            "Testing":                     {"importance": 0.65, "min_level": "intermediate", "note": "Unit testing, debugging, test-driven development"},
        },
        "certifications": [
            {"name": "AWS Certified Developer",         "provider": "Amazon",    "cost": "₹12,000-15,000", "duration": "3-4 months", "value": "High"},
            {"name": "Google Cloud Professional",       "provider": "Google",    "cost": "₹15,000-18,000", "duration": "4-5 months", "value": "High"},
            {"name": "Oracle Java Certification",       "provider": "Oracle",    "cost": "₹8,000-12,000",  "duration": "2-3 months", "value": "Medium"},
        ]
    },

    "Product Manager": {
        "description": "Defines product strategy and roadmap, works with cross-functional teams",
        "required_skills": {
            "Product Strategy":   {"importance": 0.90, "min_level": "intermediate", "note": "Market analysis, roadmapping, competitive research"},
            "Analytics / SQL":    {"importance": 0.85, "min_level": "intermediate", "note": "Data-driven decision making, metrics, KPIs"},
            "Communication":      {"importance": 0.95, "min_level": "advanced",     "note": "Stakeholder management, presentations, PRDs"},
            "User Research":      {"importance": 0.80, "min_level": "intermediate", "note": "User interviews, surveys, usability testing"},
            "Technical Knowledge":{"importance": 0.70, "min_level": "beginner",     "note": "APIs, software development understanding"},
            "Project Management": {"importance": 0.75, "min_level": "intermediate", "note": "Agile, Scrum, roadmap planning, prioritization"},
            "Design Thinking":    {"importance": 0.70, "min_level": "intermediate", "note": "Wireframing, prototyping, UX principles"},
        },
        "certifications": [
            {"name": "Product Management Certification", "provider": "Product School", "cost": "₹50,000-1,00,000", "duration": "8-12 weeks", "value": "Medium"},
            {"name": "PMP Certification",                "provider": "PMI",            "cost": "₹20,000-30,000",   "duration": "6 months",   "value": "High"},
        ]
    },

    "Data Scientist": {
        "description": "Builds ML models, analyzes complex data, creates predictive analytics",
        "required_skills": {
            "Python":               {"importance": 0.95, "min_level": "advanced",     "note": "Primary language for data science"},
            "Machine Learning":     {"importance": 0.90, "min_level": "intermediate", "note": "Scikit-learn, supervised/unsupervised learning"},
            "Statistics":           {"importance": 0.90, "min_level": "advanced",     "note": "Probability, hypothesis testing, Bayesian methods"},
            "SQL":                  {"importance": 0.80, "min_level": "intermediate", "note": "Data extraction, complex queries"},
            "Deep Learning":        {"importance": 0.75, "min_level": "beginner",     "note": "TensorFlow, PyTorch, neural networks"},
            "Data Visualization":   {"importance": 0.75, "min_level": "intermediate", "note": "Matplotlib, Seaborn, Plotly"},
            "Feature Engineering":  {"importance": 0.80, "min_level": "intermediate", "note": "Data preprocessing, feature selection"},
            "Big Data":             {"importance": 0.65, "min_level": "beginner",     "note": "Spark, Hadoop (important for senior roles)"},
        },
        "certifications": [
            {"name": "IBM Data Science Professional",        "provider": "Coursera",      "cost": "₹3,000-5,000",   "duration": "4-6 months",  "value": "High"},
            {"name": "TensorFlow Developer Certificate",     "provider": "Google",        "cost": "₹8,000-10,000",  "duration": "3-4 months",  "value": "High"},
            {"name": "AWS Machine Learning Specialty",       "provider": "Amazon",        "cost": "₹15,000-20,000", "duration": "4-6 months",  "value": "Very High"},
        ]
    },

    "Business Analyst": {
        "description": "Bridges business needs and technical solutions through analysis",
        "required_skills": {
            "SQL":                   {"importance": 0.85, "min_level": "intermediate", "note": "Query data for business insights"},
            "Excel":                 {"importance": 0.90, "min_level": "advanced",     "note": "Financial modeling, complex analysis"},
            "Requirements Gathering":{"importance": 0.85, "min_level": "intermediate", "note": "Document and analyze business requirements"},
            "Process Modeling":      {"importance": 0.75, "min_level": "intermediate", "note": "Flowcharts, BPMN, process optimization"},
            "Communication":         {"importance": 0.80, "min_level": "advanced",     "note": "Present findings clearly to stakeholders"},
            "Power BI / Tableau":    {"importance": 0.70, "min_level": "intermediate", "note": "Business intelligence reporting"},
            "Domain Knowledge":      {"importance": 0.70, "min_level": "beginner",     "note": "BFSI, retail, healthcare – industry context"},
        },
        "certifications": [
            {"name": "CBAP – Certified BA Professional", "provider": "IIBA",     "cost": "₹30,000-40,000", "duration": "6 months",   "value": "High"},
            {"name": "Google Data Analytics",            "provider": "Coursera", "cost": "₹3,000-5,000",   "duration": "6 months",   "value": "Medium"},
        ]
    },

    "Digital Marketing Specialist": {
        "description": "Plans and executes digital marketing campaigns across various channels",
        "required_skills": {
            "SEO / SEM":             {"importance": 0.85, "min_level": "intermediate", "note": "Search engine optimization and paid search"},
            "Google Analytics":      {"importance": 0.90, "min_level": "advanced",     "note": "Track and analyze campaign performance"},
            "Social Media Marketing":{"importance": 0.80, "min_level": "intermediate", "note": "Facebook Ads, Instagram, LinkedIn campaigns"},
            "Content Marketing":     {"importance": 0.75, "min_level": "intermediate", "note": "Content strategy, copywriting, storytelling"},
            "Email Marketing":       {"importance": 0.70, "min_level": "intermediate", "note": "Campaign design, automation, A/B testing"},
            "Excel / Data Analysis": {"importance": 0.70, "min_level": "intermediate", "note": "Campaign data analysis and reporting"},
        },
        "certifications": [
            {"name": "Google Digital Marketing Certificate", "provider": "Google",   "cost": "Free",           "duration": "40 hours",    "value": "High"},
            {"name": "HubSpot Marketing Certification",      "provider": "HubSpot",  "cost": "Free",           "duration": "3-4 weeks",   "value": "Medium"},
            {"name": "Meta Blueprint Certification",         "provider": "Meta",     "cost": "₹5,000-8,000",  "duration": "2-3 months",  "value": "Medium"},
        ]
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  SALARY DATA (Indian Market 2024-2025)
# ══════════════════════════════════════════════════════════════════════════════
SALARY_DATA = {
    "Data Analyst": {
        "base": 350000,
        "ranges": {
            "fresher": {"tier1": (300000, 450000), "tier2": (250000, 350000), "tier3": (200000, 300000), "remote": (250000, 380000)},
            "1-2":     {"tier1": (450000, 650000), "tier2": (350000, 500000), "tier3": (300000, 450000), "remote": (400000, 600000)},
            "3-5":     {"tier1": (700000, 1200000),"tier2": (550000, 900000), "tier3": (450000, 700000), "remote": (600000, 1000000)},
            "5+":      {"tier1": (1200000, 2000000),"tier2":(900000, 1500000),"tier3": (700000, 1200000),"remote": (1000000, 1800000)},
        }
    },
    "Software Engineer": {
        "base": 500000,
        "ranges": {
            "fresher": {"tier1": (400000, 700000), "tier2": (350000, 550000), "tier3": (300000, 450000), "remote": (380000, 650000)},
            "1-2":     {"tier1": (600000, 1000000),"tier2": (500000, 800000), "tier3": (400000, 650000), "remote": (600000, 950000)},
            "3-5":     {"tier1": (1000000, 2000000),"tier2":(800000, 1500000),"tier3": (650000, 1200000),"remote": (900000, 1800000)},
            "5+":      {"tier1": (1800000, 3500000),"tier2":(1400000, 2500000),"tier3":(1000000, 2000000),"remote":(1600000, 3000000)},
        }
    },
    "Product Manager": {
        "base": 800000,
        "ranges": {
            "fresher": {"tier1": (600000, 1000000),"tier2": (500000, 800000), "tier3": (400000, 650000), "remote": (550000, 900000)},
            "1-2":     {"tier1": (1000000, 1500000),"tier2":(800000, 1200000),"tier3": (650000, 1000000),"remote": (900000, 1400000)},
            "3-5":     {"tier1": (1500000, 3000000),"tier2":(1200000, 2200000),"tier3":(1000000, 1800000),"remote":(1300000, 2500000)},
            "5+":      {"tier1": (2500000, 5000000),"tier2":(2000000, 4000000),"tier3":(1500000, 3000000),"remote":(2200000, 4500000)},
        }
    },
    "Data Scientist": {
        "base": 600000,
        "ranges": {
            "fresher": {"tier1": (500000, 800000), "tier2": (400000, 650000), "tier3": (350000, 550000), "remote": (450000, 750000)},
            "1-2":     {"tier1": (800000, 1300000),"tier2": (650000, 1000000),"tier3": (550000, 850000), "remote": (750000, 1200000)},
            "3-5":     {"tier1": (1300000, 2500000),"tier2":(1000000, 1800000),"tier3":(800000, 1400000), "remote":(1100000, 2200000)},
            "5+":      {"tier1": (2000000, 4000000),"tier2":(1600000, 3200000),"tier3":(1200000, 2500000),"remote":(1800000, 3500000)},
        }
    },
    "Business Analyst": {
        "base": 400000,
        "ranges": {
            "fresher": {"tier1": (350000, 550000), "tier2": (300000, 450000), "tier3": (250000, 400000), "remote": (320000, 500000)},
            "1-2":     {"tier1": (550000, 800000), "tier2": (450000, 650000), "tier3": (400000, 550000), "remote": (500000, 750000)},
            "3-5":     {"tier1": (800000, 1500000),"tier2": (650000, 1200000),"tier3": (550000, 1000000),"remote": (700000, 1300000)},
            "5+":      {"tier1": (1400000, 2500000),"tier2":(1100000, 2000000),"tier3":(900000, 1600000), "remote":(1200000, 2200000)},
        }
    },
    "Digital Marketing Specialist": {
        "base": 300000,
        "ranges": {
            "fresher": {"tier1": (250000, 400000), "tier2": (200000, 350000), "tier3": (180000, 300000), "remote": (220000, 380000)},
            "1-2":     {"tier1": (400000, 600000), "tier2": (350000, 500000), "tier3": (300000, 450000), "remote": (380000, 560000)},
            "3-5":     {"tier1": (600000, 1200000),"tier2": (500000, 900000), "tier3": (400000, 750000), "remote": (550000, 1000000)},
            "5+":      {"tier1": (1000000, 1800000),"tier2":(800000, 1400000),"tier3": (650000, 1100000),"remote": (900000, 1600000)},
        }
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  SKILLS DATABASE (Learning Resources)
# ══════════════════════════════════════════════════════════════════════════════
SKILLS_DB = {
    "SQL": {
        "resources": [
            {"name": "SQLBolt",              "type": "Interactive Tutorial", "cost": "Free",           "duration": "2-3 weeks"},
            {"name": "Mode SQL Tutorial",    "type": "Tutorial",             "cost": "Free",           "duration": "3-4 weeks"},
            {"name": "HackerRank SQL",       "type": "Practice Platform",    "cost": "Free",           "duration": "Ongoing"},
            {"name": "LeetCode SQL",         "type": "Practice Platform",    "cost": "Free/Premium",   "duration": "Ongoing"},
        ],
        "practice_tips": "Solve 50+ SQL problems on HackerRank/LeetCode. Focus on JOINs, window functions, CTEs."
    },
    "Python": {
        "resources": [
            {"name": "Python for Everybody",        "type": "Coursera Course",      "cost": "Free to audit", "duration": "8 weeks"},
            {"name": "Automate the Boring Stuff",   "type": "Free Book + Online",   "cost": "Free",          "duration": "4-6 weeks"},
            {"name": "DataCamp Python Track",       "type": "Interactive Course",   "cost": "₹800/month",    "duration": "3-4 months"},
            {"name": "Kaggle Python Course",        "type": "Free Course",          "cost": "Free",          "duration": "2-3 weeks"},
        ],
        "practice_tips": "Focus on Pandas, NumPy, Matplotlib. Build 3-5 projects with real Kaggle datasets."
    },
    "Excel": {
        "resources": [
            {"name": "Excel Skills for Business", "type": "Coursera",          "cost": "Free to audit", "duration": "6 months"},
            {"name": "Chandoo.org",               "type": "Blog + Tutorials",  "cost": "Free",          "duration": "Self-paced"},
            {"name": "ExcelJet.net",              "type": "Formula Reference", "cost": "Free",          "duration": "Self-paced"},
        ],
        "practice_tips": "Master pivot tables, VLOOKUP/XLOOKUP, Power Query, and basic VBA macros."
    },
    "Power BI": {
        "resources": [
            {"name": "Microsoft Learn Power BI",  "type": "Official Tutorial",  "cost": "Free",           "duration": "6-8 weeks"},
            {"name": "Guy in a Cube (YouTube)",   "type": "YouTube Channel",    "cost": "Free",           "duration": "Ongoing"},
            {"name": "PL-300 Certification Prep", "type": "Exam Prep",          "cost": "₹4,000-6,000",  "duration": "3-4 months"},
        ],
        "practice_tips": "Create 5+ dashboards using public datasets. Learn DAX formulas thoroughly."
    },
    "Machine Learning": {
        "resources": [
            {"name": "Andrew Ng ML Course",          "type": "Coursera",          "cost": "Free to audit", "duration": "3 months"},
            {"name": "Hands-On ML (Book)",           "type": "Book",              "cost": "₹1,500-2,000",  "duration": "4-6 months"},
            {"name": "Kaggle ML Courses",            "type": "Free Courses",      "cost": "Free",          "duration": "2-3 months"},
            {"name": "Fast.ai",                      "type": "Free Course",       "cost": "Free",          "duration": "3-4 months"},
        ],
        "practice_tips": "Build 5+ ML projects. Participate in Kaggle competitions. Focus on practical implementation."
    },
    "Statistics": {
        "resources": [
            {"name": "Khan Academy Statistics",     "type": "Video Tutorials",   "cost": "Free",          "duration": "8-10 weeks"},
            {"name": "StatQuest (YouTube)",         "type": "YouTube Channel",   "cost": "Free",          "duration": "Ongoing"},
            {"name": "Statistics with Python",      "type": "Coursera",          "cost": "Free to audit", "duration": "3 months"},
        ],
        "practice_tips": "Apply stats to real datasets. Understand p-values, confidence intervals, A/B testing."
    },
    "Data Structures & Algorithms": {
        "resources": [
            {"name": "Striver's A2Z DSA Sheet",     "type": "Curated Problems",  "cost": "Free",          "duration": "4-6 months"},
            {"name": "LeetCode",                    "type": "Practice Platform", "cost": "Free/Premium",  "duration": "Ongoing"},
            {"name": "Abdul Bari (YouTube)",        "type": "Video Lectures",    "cost": "Free",          "duration": "Self-paced"},
            {"name": "GeeksforGeeks",               "type": "Reference + Problems","cost": "Free",        "duration": "Self-paced"},
        ],
        "practice_tips": "Solve 200+ problems. Cover arrays, strings, trees, graphs, DP. Practice daily."
    },
    "Deep Learning": {
        "resources": [
            {"name": "Deep Learning Specialization", "type": "Coursera (Andrew Ng)", "cost": "Free to audit", "duration": "4-5 months"},
            {"name": "TensorFlow Official Docs",     "type": "Documentation",        "cost": "Free",          "duration": "Self-paced"},
            {"name": "PyTorch Tutorials",            "type": "Official Tutorials",   "cost": "Free",          "duration": "2-3 months"},
        ],
        "practice_tips": "Build CNNs, RNNs, Transformers. Work on image classification and NLP projects."
    },
    "Google Analytics": {
        "resources": [
            {"name": "Google Analytics Academy",    "type": "Official Course",    "cost": "Free",          "duration": "4-6 weeks"},
            {"name": "GA4 Certification",           "type": "Free Certification", "cost": "Free",          "duration": "20-30 hours"},
        ],
        "practice_tips": "Set up GA on a real/demo site. Analyze real traffic data and create custom reports."
    },
    "Communication": {
        "resources": [
            {"name": "Toastmasters International",  "type": "Practice Club",      "cost": "₹5,000-8,000/yr","duration": "Ongoing"},
            {"name": "Coursera Communication",      "type": "Video Courses",      "cost": "Free to audit",  "duration": "4-6 weeks"},
        ],
        "practice_tips": "Practice presentations. Write clear documentation. Present your projects to others."
    },
}
