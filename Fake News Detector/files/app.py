import streamlit as st
import pickle
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import random

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fake News Detector India",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Session state — initialized right after set_page_config ──────────
if 'history'    not in st.session_state: st.session_state.history    = []
if 'real_count' not in st.session_state: st.session_state.real_count = 0
if 'fake_count' not in st.session_state: st.session_state.fake_count = 0
if 'input_text' not in st.session_state: st.session_state.input_text = ''

# ── Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f172a; color: #e2e8f0; }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #1a2e4a 100%);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin-bottom: 28px;
        border: 1px solid #2563eb33;
        box-shadow: 0 4px 24px #2563eb22;
    }
    .main-header h1 { color: #ffffff; font-size: 2.2rem; margin: 0; }
    .main-header p  { color: #93c5fd; margin: 6px 0 0 0; font-size: 1rem; }

    /* Input box */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border: 1.5px solid #2563eb55 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 32px;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af);
        transform: translateY(-1px);
    }

    /* Result cards */
    .result-real {
        background: linear-gradient(135deg, #052e16, #14532d);
        border: 2px solid #16a34a;
        border-radius: 14px;
        padding: 28px;
        text-align: center;
        margin: 20px 0;
    }
    .result-fake {
        background: linear-gradient(135deg, #450a0a, #7f1d1d);
        border: 2px solid #dc2626;
        border-radius: 14px;
        padding: 28px;
        text-align: center;
        margin: 20px 0;
    }
    .result-title { font-size: 2rem; font-weight: 800; margin: 0; }
    .result-sub   { font-size: 1rem; margin-top: 6px; opacity: 0.85; }

    /* Metric cards */
    .metric-row { display: flex; gap: 14px; margin: 16px 0; }
    .metric-card {
        background: #1e293b;
        border-radius: 12px;
        padding: 18px;
        flex: 1;
        text-align: center;
        border: 1px solid #334155;
    }
    .metric-val  { font-size: 1.8rem; font-weight: 700; color: #60a5fa; }
    .metric-label{ font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }

    /* Confidence bar container */
    .conf-bar-bg {
        background: #1e293b;
        border-radius: 8px;
        height: 18px;
        width: 100%;
        overflow: hidden;
        margin: 8px 0;
    }

    /* Info box */
    .info-box {
        background: #1e293b;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 12px 0;
        font-size: 0.93rem;
        color: #cbd5e1;
    }

    /* Sample button style */
    .sample-btn > button {
        background: #1e293b !important;
        color: #93c5fd !important;
        border: 1px solid #2563eb55 !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        padding: 6px 14px !important;
        width: auto !important;
    }

    /* History table */
    .history-item {
        background: #1e293b;
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #334155;
        font-size: 0.9rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.82rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #1e293b;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer     {visibility: hidden;}
    header     {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Text cleaning ─────────────────────────────────────────────────────
STOPWORDS = set([
    'the','a','an','and','or','but','in','on','at','to','for',
    'of','with','by','from','is','are','was','were','be','been',
    'have','has','had','this','that','these','those','it','its',
    'will','would','could','should','may','might','shall','do',
    'does','did','not','no','so','if','as','up','out','about'
])

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return ' '.join(words)


# ── Load or train model ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path = 'fake_news_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    # Train fresh if pkl not found
    return train_model()

def train_model():
    real_headlines = [
        'Government announces new education policy for rural areas',
        'RBI keeps repo rate unchanged at 6.5 percent',
        'India GDP grows at 7.2 percent in second quarter',
        'Supreme Court issues notice on electoral bonds case',
        'ISRO successfully launches satellite into orbit',
        'India wins gold medal at Commonwealth Games',
        'Parliament passes new data protection bill',
        'Mumbai receives heavy rainfall causing traffic disruptions',
        'Sensex rises 500 points amid positive global cues',
        'Health ministry reports decline in malaria cases',
        'India signs trade agreement with UAE',
        'New metro line inaugurated in Delhi',
        'Government launches scheme for women entrepreneurs',
        'IT sector adds 200000 jobs in first quarter',
        'India becomes third largest economy in Asia',
        'Flood relief operations underway in Assam',
        'Election commission announces poll dates for five states',
        'Scientists discover new species of fish in Indian Ocean',
        'India exports hit record high of 450 billion dollars',
        'New airport terminal opens in Bengaluru',
        'COVID vaccination drive extended to remote villages',
        'Government doubles farmer income support under PM-Kisan',
        'India signs climate agreement ahead of COP summit',
        'Stock market regulator SEBI introduces new trading rules',
        'National highway project completed ahead of schedule',
        'President signs ordinance on land acquisition reforms',
        'India cricket team wins test series against Australia',
        'Central bank releases new guidelines for digital payments',
        'Earthquake of magnitude 5.2 hits Himachal Pradesh no casualties',
        'University grants commission updates curriculum guidelines',
        'India launches first solar mission Aditya L1',
        'Finance minister presents interim budget in parliament',
        'Highway ministry approves 50 new expressway projects',
        'Indian army conducts successful anti-drone exercise',
        'Pollution levels drop in Delhi after odd-even scheme',
        'Government extends free food grain scheme for two years',
        'Chandrayaan 3 successfully lands on south pole of moon',
        'National education policy implementation reviewed by states',
        'India post office launches new digital banking services',
        'Tiger population increases by 200 in latest census',
        'New labour code to be implemented from next financial year',
        'Government bans single use plastic items in public places',
        'India ranks 40th in global innovation index 2024',
        'Fuel prices revised after global crude oil changes',
        'Railway ministry announces 100 new Vande Bharat trains',
        'India hosts G20 summit in New Delhi successfully',
        'Defence ministry approves purchase of fighter jets',
        'Health ministry approves new cancer treatment drug',
        'Aadhaar based payment system expanded to rural banks',
        'India wins bid to host 2036 Olympics in Ahmedabad',
    ]
    fake_headlines = [
        'Government to give free iPhone to all students before elections',
        'Drinking hot water cures all diseases including cancer doctors confirm',
        'Alien spacecraft spotted near Mumbai coast navy confirms presence',
        'Prime minister announces salary of 1 lakh rupees for all citizens',
        'Scientists prove that mobile phones cause instant death',
        'India discovers unlimited gold reserves bigger than entire world supply',
        'Government to shut down all private schools next month',
        'Eating onion daily gives complete immunity against all viruses',
        'Famous actor reveals secret government plot to control minds',
        'Moon is going to crash into earth in 2025 NASA confirms',
        'New law makes it illegal to speak English in India from January',
        'Petrol price to become zero rupees next month government announces',
        'WhatsApp messages now being read by government spy satellites',
        'Scientists confirm that 5G towers spread deadly radiation instantly',
        'India to ban all foreign companies and seize their assets',
        'Hospital secretly putting microchips in patients during surgery',
        'Famous politician caught taking bribe of 1000 crore on camera',
        'Government to abolish income tax completely from this year',
        'Mysterious illness kills 10000 people overnight in UP',
        'Water from Ganga river now proven to cure all types of cancer',
        'Election results were already decided six months before voting',
        'All banks in India to close permanently from next week',
        'Scientist fired for proving earth is actually flat',
        'Celebrity donates all wealth secretly to enemy country',
        'New chip being installed secretly in all Aadhaar cards to track people',
        'Government planning to tax citizens 90 percent of their salary',
        'Ancient temple discovered under mosque with proof of Hindu civilization',
        'Secret video shows judge taking orders from politician in court',
        'NASA proves yoga can replace food humans can survive without eating',
        'Famous vaccine causes autism confirmed by hidden WHO report',
        'New currency to replace rupee in secret meeting of billionaires',
        'All SIM cards to be cancelled unless biometric updated by tomorrow',
        'Milk adulterated with poison found in 90 percent of Indian brands',
        'Famous cricketer involved in match fixing exposed by secret source',
        'Government spy app installed on every smartphone without permission',
        'Scientists discover eating cow urine cures diabetes permanently',
        'North India to face massive earthquake of magnitude 10 tomorrow',
        'Mysterious black hole approaching earth will destroy everything in 2026',
        'Cancer cured completely by ayurvedic herb kept secret by pharma companies',
        'Secret tunnel found under parliament connecting to foreign embassy',
        'All ATMs to stop working from midnight tonight RBI denies',
        'Bollywood actress reveals government is poisoning tap water in cities',
        'Free electricity for all households announced but media hiding the news',
        'Scientists confirm coconut oil reverses ageing returns youth in 7 days',
        'India army officer leaks secret documents to Pakistan on social media',
        'Government official caught with 500 crore cash hidden in office walls',
        'School textbooks to include chapter on how to vote for ruling party',
        'Famous judge gives wrong verdict under threat from politicians family',
        'New tax on breathing oxygen proposed in secret budget meeting',
        'Flood in Chennai caused deliberately by government to hide corruption',
    ]

    texts, labels = [], []
    for h in real_headlines:
        for variant in [h, h + ' sources say', 'Breaking: ' + h]:
            texts.append(clean_text(variant))
            labels.append('real')
    for h in fake_headlines:
        for variant in [h, h + ' viral claim', 'Shocking: ' + h]:
            texts.append(clean_text(variant))
            labels.append('fake')

    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ('clf',   LogisticRegression(max_iter=1000))
    ])
    model.fit(texts, labels)
    return model


# ── Confidence bar HTML ───────────────────────────────────────────────
def confidence_bar(label, confidence):
    color  = '#16a34a' if label == 'real' else '#dc2626'
    pct    = int(confidence * 100)
    return f"""
    <div style='margin: 6px 0;'>
        <div style='display:flex; justify-content:space-between;
                    font-size:0.85rem; color:#94a3b8; margin-bottom:4px;'>
            <span>Confidence</span><span>{pct}%</span>
        </div>
        <div class='conf-bar-bg'>
            <div style='height:100%; width:{pct}%;
                        background:{color}; border-radius:8px;
                        transition: width 0.6s ease;'></div>
        </div>
    </div>"""


# ── Key word extractor ────────────────────────────────────────────────
def get_top_words(text, model, n=8):
    try:
        vec   = model.named_steps['tfidf']
        clf   = model.named_steps['clf']
        feat  = vec.transform([clean_text(text)])
        names = vec.get_feature_names_out()
        coefs = clf.coef_[0]          # positive = real, negative = fake
        nonzero = feat.nonzero()[1]
        if len(nonzero) == 0:
            return [], []
        word_scores = [(names[i], coefs[i]) for i in nonzero]
        word_scores.sort(key=lambda x: x[1], reverse=True)
        real_words = [w for w, s in word_scores if s > 0][:n]
        fake_words = [w for w, s in word_scores if s < 0][:n]
        return real_words, fake_words
    except:
        return [], []


# ── Sample headlines ──────────────────────────────────────────────────
SAMPLE_REAL = [
    "ISRO successfully launches communication satellite into geostationary orbit",
    "India GDP grows at 7.2 percent in second quarter of fiscal year",
    "Supreme Court issues notice on electoral bonds transparency case",
    "Chandrayaan 3 successfully lands on south pole of moon",
    "Railway ministry announces 100 new Vande Bharat express trains across India",
]
SAMPLE_FAKE = [
    "Government to give free iPhone 15 to all students before 2024 elections",
    "Scientists confirm that 5G towers spread deadly radiation causes instant death",
    "Moon is going to crash into earth next year NASA secretly confirms",
    "Eating raw onion daily gives complete immunity against all known viruses",
    "All bank accounts to be frozen from tomorrow midnight government silent",
]



# ═══════════════════════════════════════════════════════════════════
#  MAIN UI
# ═══════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class='main-header'>
    <h1>🔍 Fake News Detector</h1>
    <p>AI-powered news verification for India  •  Built with Python & Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Stats row
total = st.session_state.real_count + st.session_state.fake_count
st.markdown(f"""
<div class='metric-row'>
    <div class='metric-card'>
        <div class='metric-val'>{total}</div>
        <div class='metric-label'>Total Checked</div>
    </div>
    <div class='metric-card'>
        <div class='metric-val' style='color:#16a34a;'>{st.session_state.real_count}</div>
        <div class='metric-label'>✅ Real News</div>
    </div>
    <div class='metric-card'>
        <div class='metric-val' style='color:#dc2626;'>{st.session_state.fake_count}</div>
        <div class='metric-label'>❌ Fake News</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Load model
model = load_model()

# ── Sample headline buttons ───────────────────────────────────────────
st.markdown("#### 📋 Try a Sample Headline")
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Load Real News Sample"):
        st.session_state.input_text = random.choice(SAMPLE_REAL)
with col2:
    if st.button("❌ Load Fake News Sample"):
        st.session_state.input_text = random.choice(SAMPLE_FAKE)

st.markdown("<br>", unsafe_allow_html=True)

# ── Text input ────────────────────────────────────────────────────────
st.markdown("#### ✍️ Enter a News Headline or Article")
news_input = st.text_area(
    label     = "",
    value     = st.session_state.input_text,
    height    = 130,
    max_chars = 1000,
    placeholder = "Paste a news headline or short article here...\n\nExample: ISRO successfully launches satellite into orbit",
)

word_count = len(news_input.split()) if news_input.strip() else 0
st.caption(f"📝 {word_count} words  •  {len(news_input)} characters")

# ── Analyse button ────────────────────────────────────────────────────
analyse_clicked = st.button("🔍  Analyse This News", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────
if analyse_clicked:
    if not news_input.strip():
        st.warning("⚠️ Please enter some text first!")
    elif word_count < 3:
        st.warning("⚠️ Please enter at least a few words for accurate analysis.")
    else:
        with st.spinner("Analysing with AI..."):
            cleaned   = clean_text(news_input)
            label     = model.predict([cleaned])[0]
            proba     = model.predict_proba([cleaned])[0]
            classes   = model.classes_
            conf_dict = dict(zip(classes, proba))
            confidence = conf_dict[label]

            # Update session counts
            if label == 'real':
                st.session_state.real_count += 1
            else:
                st.session_state.fake_count += 1

            # Save to history
            short = news_input[:60] + '...' if len(news_input) > 60 else news_input
            st.session_state.history.insert(0, {
                'text':       short,
                'label':      label,
                'confidence': confidence
            })
            if len(st.session_state.history) > 10:
                st.session_state.history = st.session_state.history[:10]

        # ── Result card ──────────────────────────────────────────────
        if label == 'real':
            st.markdown(f"""
            <div class='result-real'>
                <div class='result-title'>✅ REAL NEWS</div>
                <div class='result-sub'>This news appears to be legitimate</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='result-fake'>
                <div class='result-title'>❌ FAKE NEWS</div>
                <div class='result-sub'>This news shows signs of being false or misleading</div>
            </div>
            """, unsafe_allow_html=True)

        # Confidence bar
        st.markdown(confidence_bar(label, confidence), unsafe_allow_html=True)

        # ── Confidence breakdown chart ───────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 Confidence Breakdown")

        fig, ax = plt.subplots(figsize=(7, 2.5))
        fig.patch.set_facecolor('#1e293b')
        ax.set_facecolor('#1e293b')

        categories = ['Real News', 'Fake News']
        values     = [conf_dict.get('real', 0)*100, conf_dict.get('fake', 0)*100]
        colors_bar = ['#16a34a', '#dc2626']

        bars = ax.barh(categories, values, color=colors_bar,
                       height=0.45, edgecolor='none')
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}%', va='center', color='#e2e8f0',
                    fontsize=11, fontweight='bold')

        ax.set_xlim(0, 115)
        ax.set_xlabel('Confidence (%)', color='#94a3b8', fontsize=9)
        ax.tick_params(colors='#e2e8f0', labelsize=10)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.xaxis.label.set_color('#94a3b8')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # ── Keyword analysis ─────────────────────────────────────────
        real_words, fake_words = get_top_words(news_input, model)
        if real_words or fake_words:
            st.markdown("#### 🔑 Key Words Analysis")
            kc1, kc2 = st.columns(2)
            with kc1:
                st.markdown("**✅ Words suggesting REAL:**")
                if real_words:
                    for w in real_words[:5]:
                        st.markdown(
                            f"<span style='background:#052e16; color:#4ade80;"
                            f"padding:3px 10px; border-radius:20px; "
                            f"font-size:0.85rem; margin:3px; display:inline-block;'>"
                            f"{w}</span>", unsafe_allow_html=True)
                else:
                    st.caption("None found")
            with kc2:
                st.markdown("**❌ Words suggesting FAKE:**")
                if fake_words:
                    for w in fake_words[:5]:
                        st.markdown(
                            f"<span style='background:#450a0a; color:#f87171;"
                            f"padding:3px 10px; border-radius:20px; "
                            f"font-size:0.85rem; margin:3px; display:inline-block;'>"
                            f"{w}</span>", unsafe_allow_html=True)
                else:
                    st.caption("None found")

        # ── Advice box ───────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        if label == 'fake':
            st.markdown("""
            <div class='info-box'>
            ⚠️ <b>What to do with fake news:</b><br>
            • Do not share this on WhatsApp or social media<br>
            • Check trusted sources like ANI, PTI, NDTV, or The Hindu<br>
            • Verify on fact-checking sites: AltNews.in, Boom Live, FactChecker.in<br>
            • Report to cybercrime portal: cybercrime.gov.in
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='info-box'>
            ✅ <b>This looks real — but always verify:</b><br>
            • Cross-check with at least 2-3 trusted news sources<br>
            • Check if the source has a verifiable URL and author<br>
            • Look for a date — old news can be reshared out of context<br>
            • Trust official sources: pib.gov.in, isro.gov.in, rbi.org.in
            </div>
            """, unsafe_allow_html=True)

# ── History section ───────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown("#### 🕐 Recent Analysis History")
    for item in st.session_state.history[:5]:
        icon  = '✅' if item['label'] == 'real' else '❌'
        color = '#16a34a' if item['label'] == 'real' else '#dc2626'
        label = item['label'].upper()
        conf  = int(item['confidence'] * 100)
        st.markdown(f"""
        <div class='history-item'>
            <span style='color:#cbd5e1; flex:1;'>{item['text']}</span>
            <span style='color:{color}; font-weight:700;
                         margin-left:12px; white-space:nowrap;'>
                {icon} {label} ({conf}%)
            </span>
        </div>
        """, unsafe_allow_html=True)

    col_clear, _ = st.columns([1, 3])
    with col_clear:
        if st.button("🗑️ Clear History"):
            st.session_state.history    = []
            st.session_state.real_count = 0
            st.session_state.fake_count = 0
            st.rerun()

# ── Pie chart of session stats ────────────────────────────────────────
total = st.session_state.real_count + st.session_state.fake_count
if total >= 2:
    st.markdown("---")
    st.markdown("#### 📈 Your Session Summary")
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    fig2.patch.set_facecolor('#1e293b')
    ax2.set_facecolor('#1e293b')
    sizes  = [st.session_state.real_count, st.session_state.fake_count]
    colors = ['#16a34a', '#dc2626']
    labels = [f'Real ({st.session_state.real_count})',
              f'Fake ({st.session_state.fake_count})']
    wedges, texts, autotexts = ax2.pie(
        sizes, labels=labels, colors=colors,
        autopct='%1.0f%%', startangle=140,
        textprops={'color': '#e2e8f0', 'fontsize': 11},
        wedgeprops={'edgecolor': '#0f172a', 'linewidth': 2}
    )
    for at in autotexts:
        at.set_color('#ffffff')
        at.set_fontweight('bold')
    ax2.set_title("News Analysed This Session",
                  color='#94a3b8', fontsize=10, pad=12)
    st.pyplot(fig2)
    plt.close()

# ── How it works section ──────────────────────────────────────────────
st.markdown("---")
with st.expander("🤖 How Does This Work? (For Interviews & Viva)"):
    st.markdown("""
    ### Machine Learning Pipeline

    **Step 1 — Data Collection**
    The model was trained on hundreds of real and fake news headlines
    specific to the Indian context.

    **Step 2 — Text Preprocessing**
    Raw text is cleaned by converting to lowercase, removing punctuation,
    numbers, and common stopwords (the, a, an, is...).

    **Step 3 — TF-IDF Vectorization**
    Text is converted into numbers using **TF-IDF** (Term Frequency –
    Inverse Document Frequency). Words that appear often in fake news
    but rarely in real news get high scores — and vice versa.
    Bigrams (2-word combinations) are also captured.

    **Step 4 — Logistic Regression Classifier**
    A Logistic Regression model learns the pattern between word scores
    and the real/fake label. It outputs a **probability** for each class.

    **Step 5 — Prediction**
    New text is cleaned → vectorized → fed into the model →
    it returns REAL or FAKE with a confidence percentage.

    ---
    **Tech Stack:**
    `Python` · `Scikit-learn` · `TF-IDF` · `Logistic Regression` · `Streamlit`

    **Key Concept:** The model learns that words like *"secretly", "confirms",
    "shocking", "cure all"* are more common in fake news, while words like
    *"parliament", "ministry", "percent", "launched"* appear more in real news.
    """)

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    🔍 Fake News Detector India  •  Built by Manish Kumar  •  B.Tech CSE 3rd Year<br>
    Shobhasariya Group of Institution, Sikar  •  Made with Python & Machine Learning 🐍
</div>
""", unsafe_allow_html=True)