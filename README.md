# 💰 Personal Finance Analyzer (AI-Powered)

An AI-powered Personal Finance Analyzer that processes Google Pay transaction statements, performs intelligent analysis using Machine Learning, and provides insights, anomaly detection, and future spending predictions.

---

## 🚀 Features

* 📂 Upload Google Pay CSV statements
* 🧹 Automatic data cleaning & preprocessing
* 🤖 ML-based expense categorization
* 🚨 Anomaly detection (unusual spending)
* 📊 Monthly spending analytics
* 📈 Future spending prediction (ML model)
* 🔐 Secure authentication using Supabase (JWT)
* ☁️ Cloud database (Supabase)
* ⚡ FastAPI backend (high performance)

---

## 🧠 Tech Stack

### Backend

* FastAPI
* Python
* Pandas

### Machine Learning

* Scikit-learn
* TF-IDF (NLP)
* RandomForest (classification)
* IsolationForest (anomaly detection)
* Linear Regression (prediction)

### Database & Auth

* Supabase (PostgreSQL + Auth)

### DevOps

* Render (deployment)

---

## 🏗️ Architecture

```
Frontend (React)
        ↓
FastAPI Backend
        ↓
Supabase (DB + Auth)
        ↓
ML Models (Classification + Prediction)
```

---

## 📂 Project Structure

```
app/
 ├── main.py
 ├── routes/
 ├── services/
 ├── db/
 ├── ml/
 ├── utils/
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone Repo

```
git clone https://github.com/your-username/Personal-Finance-Analyzer.git
cd Personal-Finance-Analyzer
```

---

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create `.env` file:

```
SUPABASE_URL=your_url
SUPABASE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret
```

---

### 5. Train ML Model

```
python app/ml/train_model.py
```

---

### 6. Run Server

```
python3 -m uvicorn app.main:app --reload
```

---

## 🌐 API Endpoints

### 📤 Upload Transactions

```
POST /upload-transactions
```

---

### 📊 Get Analytics

```
GET /analytics
```

Returns:

* Total spending
* Category breakdown
* Monthly trends
* Anomalies
* Future prediction

---

## 📊 Example Output

```
{
  "total_spent": 5000,
  "category_breakdown": {
    "Food": 1200,
    "Shopping": 2000
  },
  "monthly_trend": {
    "2026-03": 5000
  },
  "prediction": {
    "predicted_spending_next_month": 5800
  },
  "anomalies": [
    {
      "description": "Amazon Shopping",
      "amount": -5000
    }
  ]
}
```

---

## 🔐 Authentication

* Uses Supabase JWT
* All endpoints are protected
* Requires Bearer token

---

## 🚀 Deployment

Backend deployed on Render:

```
https://personal-finance-analyzer-20ce.onrender.com
```

---

## 🧠 ML Models

### 1. Expense Classification

* Input: transaction description
* Output: category
* Model: RandomForest + TF-IDF

### 2. Anomaly Detection

* Model: IsolationForest

### 3. Spending Prediction

* Model: Linear Regression

---

## ⚡ Future Improvements

* 📱 Mobile app (Flutter)
* 📊 Advanced dashboards
* 🤖 AI financial advisor (LLM)
* 📉 Budget recommendations
* 📈 Category-wise prediction

---

## 👨‍💻 Author

**Vishal Songara**

---

## ⭐ Contribute

Feel free to fork and improve this project 🚀
