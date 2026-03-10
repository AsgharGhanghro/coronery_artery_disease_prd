# 🫀 CAD CheckUp — Coronary Artery Disease Risk Predictor

> A full-stack AI-powered web application that predicts Coronary Artery Disease (CAD) risk using a trained machine learning model and an interactive 11-step clinical questionnaire.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=flat-square&logo=flask)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Frontend-06B6D4?style=flat-square&logo=tailwindcss)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-FF6384?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

> ⚠️ **Medical Disclaimer:** This tool is for educational and informational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## 📸 Preview

The app guides users through an 11-question clinical wizard, computes a logistic regression risk score on the frontend (with a trained `.pkl` model on the backend), and renders a full Heart Health Report with an interactive analytics dashboard.

---

## 🗂️ Project Structure

```
CAD/
├── client/
│   ├── index.html           # Main assessment wizard (11-step form + results modal)
│   └── dashboard.html       # Standalone analytics dashboard page
│
├── data/
│   └── Coronary_artery.csv  # Cleveland Heart Disease dataset (UCI)
│
├── Server/
│   ├── artifacts/
│   │   ├── best_coronary_artery_model.pkl  # Best trained model (serialized)
│   │   ├── coronary_model.pkl              # Base trained model (serialized)
│   │   ├── CAD.ipynb                       # Model training notebook
│   │   └── Coronary_artery.json            # Dataset metadata / schema
│   ├── create_simple_model.py  # Script to train and export the ML model
│   ├── dashboard_api.py        # API endpoints for dashboard analytics
│   ├── server.py               # Main Flask application entry point
│   ├── run.py                  # Server runner / startup script
│   ├── utils.py                # Helper functions (preprocessing, feature encoding)
│   ├── test_api.py             # API unit tests
│   └── requirements.txt        # Python dependencies
│
├── .gitignore
└── vercel.json                 # Vercel deployment config
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧙 **11-Step Wizard** | Step-by-step clinical questionnaire with back/next navigation and validation |
| 🧠 **ML Risk Scoring** | Logistic regression model trained on the Cleveland Heart Disease dataset |
| 📊 **Risk Report** | Score (0–10), probability %, risk tier (Low / Moderate / High), and 5 personalized directives |
| 📈 **Analytics Dashboard** | 4 Chart.js charts — doughnut, bar, radar, and population comparison line chart |
| ♾️ **Insights Feed** | Infinite-scroll health education cards loaded in batches |
| 🖨️ **Print & Export** | Print the full report or copy raw JSON to clipboard |
| ✨ **3D Parallax Card** | The wizard card tilts on mouse movement using CSS perspective transforms |
| 📱 **Responsive** | Works on mobile, tablet, and desktop |
| 🔁 **Graceful Fallback** | If the Flask backend is unreachable, the frontend computes the score locally using embedded logistic regression coefficients |

---

## 🩺 Clinical Inputs (Questions)

| # | Field | Type | Range |
|---|---|---|---|
| 1 | Age | Number | 20 – 100 years |
| 2 | Gender | Select | Female / Male |
| 3 | Resting Blood Pressure | Number | 80 – 220 mm Hg |
| 4 | Serum Cholesterol | Number | 100 – 600 mg/dL |
| 5 | Max Heart Rate Achieved | Number | 60 – 220 bpm |
| 6 | Chest Pain Type | Select | Typical / Atypical / Non-anginal / Asymptomatic |
| 7 | Exercise Induced Angina | Select | Yes / No |
| 8 | Fasting Blood Sugar | Select | ≤120 mg/dL / >120 mg/dL |
| 9 | Resting ECG | Select | Normal / ST-T Abnormality / LV Hypertrophy |
| 10 | ST Depression (exercise) | Number | 0 – 6.2 mm |
| 11 | Major Vessels (fluoroscopy) | Select | 0 / 1 / 2 / 3 |

---

## 🔬 How the Model Works

### Feature Encoding

Raw user inputs are mapped to numeric values matching the UCI Cleveland dataset format:

```
gender    → sex:      female=0, male=1
chest_pain → cp:      typical=0, atypical=1, nonanginal=2, asymptomatic=3
blood_sugar → fbs:    normal=0, elevated=1
ecg       → restecg:  normal=0, abnormal=1, hypertrophy=2
exercise_angina → exang: no=0, yes=1
vessels   → ca:       none=0, one=1, two=2, three=3
```

### Logistic Regression (Frontend Fallback Coefficients)

```
intercept  = -5.47
age        = +0.031    sex       = +0.92
cp         = +0.71     trestbps  = +0.014
chol       = +0.004    fbs       = +0.41
restecg    = +0.34     thalach   = -0.023
exang      = +0.84     oldpeak   = +0.55
ca         = +0.94
```

```
logit = intercept + Σ(coef × feature)
probability = 1 / (1 + e^(-logit))
score (0–10) = min(round(probability × 10), 10)
```

### Risk Tiers

| Score | Level | Recommendations | Next Check |
|---|---|---|---|
| 0 – 3 | 🟢 Low | Lifestyle maintenance | 12 months |
| 4 – 6 | 🟡 Moderate | GP review within 4 weeks | 6 months |
| 7 – 10 | 🔴 High | Cardiologist within 48 hours | 3 months |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CAD-CheckUp.git
cd CAD-CheckUp
```

### 2. Install Python dependencies

```bash
cd Server
pip install -r requirements.txt
```

### 3. Train the model (optional — pre-trained `.pkl` files are included)

```bash
python create_simple_model.py
```

This reads `data/Coronary_artery.csv`, trains the model, and saves `artifacts/best_coronary_artery_model.pkl`.

### 4. Start the Flask server

```bash
python run.py
# or
python server.py
```

Server runs at `http://127.0.0.1:5000`

### 5. Open the app

Open `client/index.html` in your browser, or navigate to `http://127.0.0.1:5000`.

---

## 🔌 API Endpoints

### `POST /predict`

Runs the trained model and returns a risk prediction.

**Request:**
```json
{
  "age": 55, "sex": 1, "cp": 2, "trestbps": 140,
  "chol": 250, "fbs": 0, "restecg": 1, "thalach": 145,
  "exang": 1, "oldpeak": 2.3, "ca": 1
}
```

**Response:**
```json
{
  "probability": 0.72,
  "score": 7,
  "level": "high",
  "recommendations": ["See a cardiologist within 48 h", "..."]
}
```

---

### `GET /dashboard/stats`

Returns aggregated statistics for the analytics dashboard (served by `dashboard_api.py`).

---

### `GET /health`

Health check endpoint.

```json
{ "status": "ok" }
```

---

## 📊 Dashboard Charts

| Chart | Type | Description |
|---|---|---|
| Risk Distribution | Doughnut | Population split across Low / Moderate / High tiers |
| Key Risk Factors | Bar | Per-feature impact score (0–10) derived from user inputs |
| Health Metrics | Radar | User's 5 metrics vs. healthy range baseline |
| Population Comparison | Line | User's probability plotted against age-group averages |

---

## 🗃️ Dataset

**Cleveland Heart Disease Dataset** — UCI Machine Learning Repository

- **File:** `data/Coronary_artery.csv`
- **Records:** 303 patients
- **Features:** 13 clinical attributes + 1 binary target (disease present/absent)
- **Source:** [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3, Flask |
| ML | scikit-learn (Logistic Regression), joblib (`.pkl` serialization) |
| Notebook | Jupyter (`CAD.ipynb`) |
| Frontend | Vanilla HTML/JS, Tailwind CSS (CDN) |
| Charts | Chart.js |
| Icons | Font Awesome 6 |
| Fonts | Google Fonts — Inter |
| Deployment | Vercel (`vercel.json`) |

---

## 🚢 Deployment (Vercel)

The project includes a `vercel.json` config for serverless deployment.

```bash
npm install -g vercel
vercel
```

Ensure your Flask routes are configured as serverless functions or use a WSGI adapter such as `flask-lambda` / `mangum` depending on the Vercel setup.

---

## 👥 Authors

- **Ali** — ML model development, Flask backend, data pipeline


---

## 📄 License

MIT — free to use, fork, and build upon.
