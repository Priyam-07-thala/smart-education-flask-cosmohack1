# 🎓 SMART EDUCATION MODEL

An AI‑powered web application built with **Flask** to help teachers identify **at‑risk students** and help students track their academic performance.  
This project was developed as part of a **24‑hour hackathon** with a focus on **education, analytics, and early intervention**.

---

## 🚀 Features

### 👩‍🏫 Teacher Module
- Secure login & signup
- Upload student data via **CSV**
- Automatic **risk prediction** (Low / Medium / High)
- View all students in a dashboard
- Detailed student performance report with charts

### 🎓 Student Module
- Secure login & signup
- Personalized dashboard
- Performance visualization (attendance, marks, assignments, behavior)
- Risk status display

### 🤖 ML Integration
- Data preprocessing
- Trained ML model (`model.pkl`)
- Risk classification based on academic indicators

---

## 🧠 Tech Stack

| Layer | Technology |
|-----|-----------|
| Backend | Flask (Python) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| ML | Scikit‑learn |
| Deployment | Free cloud platforms (Render / Railway) |

---

## 📁 Project Structure

```text
SMART-EDUCATION-MODEL
├─ backend/
│  ├─ ml/
│  │  ├─ model.pkl
│  │  ├─ preprocess.py
│  │  └─ train_model.py
│  │
│  ├─ static/
│  │  ├─ charts/
│  │  ├─ css/
│  │  │  └─ style.css
│  │  ├─ images/
│  │  ├─ js/
│  │  │  ├─ dragdrop.js
│  │  │  └─ theme.js
│  │  └─ uploads/
│  │
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ login.html
│  │  ├─ signup.html
│  │  ├─ role_select.html
│  │  ├─ teacher_dashboard.html
│  │  ├─ student_dashboard.html
│  │  └─ student_report.html
│  │
│  ├─ app.py
│  ├─ database.db
│  └─ .gitignore
│
├─ data/
│  ├─ sample_student_1.csv
│  └─ StudentsPerformance.csv
│
├─ requirements.txt
└─ README.md

## 📊 CSV Format (Required)

