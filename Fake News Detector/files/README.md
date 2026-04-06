# 🔍 Fake News Detector India

> An AI-powered fake news detection web app built with Python and Machine Learning — designed specifically for the Indian news context.

![Python]
![Streamlit]
![Scikit-learn]
![License]

---

## 🚀 Live Demo,

👉 **[Click here to try the app](not here till)**

---

## 📸 Screenshots,

| Home Screen | Real News Result | Fake News Result |

| Enter headline | ✅ Green card | ❌ Red card |



## 🎯 What It Does, 

Paste any news headline or short article and the app instantly tells you:

-  **REAL** or ❌ **FAKE** with a confidence percentage
-  Visual confidence breakdown chart
-  Key words that influenced the decision
-  What to do next (fact-check links, official sources)
-  Session history of all checked news
-  Pie chart of your session summary


## 🛠️ Tech Stack,

| Technology                    | Purpose 
|
| Python                   Core programming language 
| Scikit-learn             ML model (Logistic Regression)
| TF-IDF Vectorizer        Convert text to numbers
| Streamlit                Web app interface 
| Matplotlib               Charts and visualizations 
| Pickle                   Save and load trained model 


##  How It Works

```
Raw News Text
      ↓
Text Cleaning (lowercase, remove punctuation, stopwords)
      ↓
TF-IDF Vectorization (convert words to numbers + bigrams)
      ↓
Logistic Regression Classifier
      ↓
REAL or FAKE  +  Confidence %
```

**Key Concept:** The model learns that words like *"secretly", "shocking", "cure all", "confirms"* appear more in fake news, while words like *"parliament", "ministry", "launched", "percent"* appear more in real news.

---

## 📁 Project Structure

```
fake-news-detector/
│
├── app.py                  # Main Streamlit application
├── fake_news_model.pkl     # Trained ML model (auto-generated)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```



## 👨‍💻 About

**Manish Kumar** — B.Tech CSE, 3rd Year  
Shobhasariya Group of Institution, Sikar  
GitHub: [@manishkumar-cmd](https://github.com/manishkumar-cmd)

---

## ⭐ If you found this useful, please give it a star!

> *Built to fight misinformation in India, one headline at a time.* 🇮🇳
