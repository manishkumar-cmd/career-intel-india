
# 🔍 Fake News Detector India

So I built this project because honestly, I was tired of seeing random WhatsApp forwards being treated as breaking news. You know the ones — "Government giving free iPhone to all students!" or "Drinking hot water cures cancer, doctors confirm!" — and somehow people actually believe and share this stuff.

As a CSE student, I thought — why not actually do something about it? So I built a tool that uses Machine Learning to detect whether a news headline is real or fake. It's not perfect, but it works pretty well and it was a great learning experience.

---

## 🚀 Live Demo

👉 **[Try it here](https://your-app-link.streamlit.app)** ← *(deploy on Streamlit Cloud for free and paste your link here)*

---

## 📸 What It Looks Like

The app has a clean dark UI. You paste a headline, hit analyse, and it tells you:

- ✅ **REAL** — shown in green with confidence percentage
- ❌ **FAKE** — shown in red with confidence percentage

Plus it shows you a bar chart, the keywords that influenced the decision, and some advice on what to do next.

---

## 💡 Why I Built This

Fake news is a massive problem in India especially on WhatsApp and social media. Most fact-checking websites require you to manually search for a claim. I wanted something faster — paste the headline, get the answer in seconds.

Also this was my first real ML + web app project and I learned a ton building it.

---

## 🛠️ Tech Stack

Nothing fancy — just Python and some libraries I learned during my course:

- **Python** — core language
- **Scikit-learn** — for the ML model (Logistic Regression)
- **TF-IDF Vectorizer** — converts text into numbers the model can understand
- **Streamlit** — turns the Python script into a working web app (honestly Streamlit is amazing for this)
- **Matplotlib** — for the confidence charts
- **Pickle** — to save and load the trained model

---

## 🧠 How It Actually Works

This is the part I find most interesting and also what my teacher asked me about in the viva 😄

```
You type a headline
        ↓
Text gets cleaned  →  lowercase, remove punctuation, remove stopwords
        ↓
TF-IDF converts words into numbers  →  bigrams also captured
        ↓
Logistic Regression predicts:  REAL or FAKE
        ↓
Output:  Label  +  Confidence %  +  Key words  +  Chart
```

**The key idea behind TF-IDF:**
Words like *"secretly", "shocking", "confirms", "cure all", "free iPhone"* appear a lot in fake news. Words like *"parliament", "ministry", "launched", "percent", "ISRO"* appear more in real news. The model learns these patterns during training and uses them to make predictions on new text.

---

## 📁 Project Structure

```
fake-news-detector/
│
├── app.py                 →  the entire web application
├── fake_news_model.pkl    →  trained ML model (auto-generated on first run)
├── requirements.txt       →  all dependencies
└── README.md              →  you're reading it
```

---

## ⚙️ Run It Yourself

**Step 1 — Clone the repo**
```bash
git clone https://github.com/manishkumar-cmd/fake-news-detector.git
cd fake-news-detector
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**

> ⚠️ Important — do NOT run it with `python app.py`. That won't work.
> You MUST use the streamlit command below:

```bash
streamlit run app.py
```

**Step 4 — Open browser**

It will automatically open at:
```
http://localhost:8501
```

---

## ☁️ Deploy for Free on Streamlit Cloud

1. Push this repo to your GitHub
2. Go to **[share.streamlit.io](https://share.streamlit.io)**
3. Sign in with GitHub
4. Select this repo and choose `app.py` as the main file
5. Click **Deploy**

You get a free permanent link like `your-app.streamlit.app` — perfect for putting on your resume!

---

## 📊 Model Details

| Thing | Detail |
|---|---|
| Algorithm | Logistic Regression |
| Text Features | TF-IDF with bigrams |
| Max Features | 5000 |
| Training Data | India-specific real and fake headlines |
| Classes | `real` / `fake` |

The model is trained on headlines specifically written for the Indian context — government news, ISRO, cricket, WhatsApp-style fake claims etc. This makes it much more relevant than generic English datasets.

---

## ⚠️ Limitations (being honest here)

- The model was trained on a relatively small dataset — it works well on obvious cases but might struggle with subtle misinformation
- It only looks at the text, not the source URL or author
- It works best with English headlines — Hindi or Hinglish may not give accurate results
- It's not a replacement for proper fact-checking — always verify important news on AltNews or BoomLive

---

## 🔮 What I Want to Add Later

- [ ] Support for full article text, not just headlines
- [ ] Input a URL and check the article directly
- [ ] Hindi language support
- [ ] Train on a larger dataset (Kaggle has 40k+ fake news articles)
- [ ] Show which fact-checking site has already covered the story

---

## 🤝 Contributing

If you want to improve the dataset or model, feel free to fork and send a PR. Any contributions are welcome especially around:
- Adding more Indian-context training examples
- Improving the UI
- Adding multilingual support

---

## 📬 Contact

**Manish Kumar**
B.Tech CSE — 3rd Year
Shobhasariya Group of Institution, Sikar

GitHub: [@manishkumar-cmd](https://github.com/manishkumar-cmd)

---

## ⭐ Star This Repo

If this helped you or you found it interesting, please give it a star. It genuinely motivates me to keep building more projects like this.

---

*Built because fake news on WhatsApp was getting out of hand. 🇮🇳*
