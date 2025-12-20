# Live Website
Live URL: https://student-at-risk-prediction.onrender.com

## How to run the website
### for teacher login: 
username: teacher_1
password: teacher_1

### for student login
username:student_23
password:student_23

these are samples data which we have given

You can also signup but remember the studentID.
## .csv file format -
### student_id,name,attendance,avg_marks,assignment_completion,behavior_score

#### Remember the studentId as when signup in the site you have give that studentId which was given by the teacher

#### 1. attendance,avg_marks,assignment_completion- range is (0,100)
#### 2. behavior_score- range is (0,10)




# 🎓 Smart Education Model (Flask-Based Web App)

A **Smart Education Model** built using **Flask**, designed to help teachers monitor student performance and predict academic risk based on multiple parameters such as attendance, marks, assignments, and behavior.

This project was developed with a **24‑hour hackathon mindset**, focusing on clarity, usability, and real-world applicability in educational institutions.

---

## 🚀 Features

### 👩‍🏫 Teacher Module
- Secure login & signup
- Upload student data using **CSV (Drag & Drop supported)**
- Automatic **risk prediction** (Low / Medium / High)
- View complete student performance table
- Individual student performance report

### 🎓 Student Module
- Secure login & signup
- Personalized dashboard
- Visual performance indicators
- Risk status display

### 📊 Risk Calculation Parameters
- Attendance
- Average Marks
- Assignment Completion
- Behavior Score

---

## 🛠 Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **ML (Optional):** Scikit‑Learn (pretrained model)
- **Version Control:** Git & GitHub

```
SMART-EDUCATION-MODEL
├─ backend/
│ ├─ ml/
│ │ ├─ init.py
│ │ ├─ preprocess.py
│ │ ├─ train_model.py
│ │ └─ model.pkl
│ ├─ static/
│ │ ├─ charts/
│ │ │ └─ student_chart.png
│ │ ├─ css/
│ │ │ └─ style.css
│ │ ├─ images/
│ │ │ ├─ login_bg.jpg
│ │ │ ├─ role_bg.jpg
│ │ │ ├─ signup_bg.jpg
│ │ │ ├─ student_bg.jpg
│ │ │ └─ teacher_bg.jpg
│ │ ├─ js/
│ │ │ ├─ dragdrop.js
│ │ │ └─ theme.js
│ │ └─ uploads/
│ │ ├─ sample_student_1.csv
│ │ └─ sample_students.csv
│ ├─ templates/
│ │ ├─ base.html
│ │ ├─ login.html
│ │ ├─ role_select.html
│ │ ├─ signup.html
│ │ ├─ student_dashboard.html
│ │ ├─ student_report.html
│ │ └─ teacher_dashboard.html
│ ├─ .gitignore
│ ├─ app.py
│ └─ database.db
│
├─ data/
│ ├─ sample_student_1.csv
│ └─ StudentsPerformance.csv
│
├─ database.db
└─ requirements.txt

```

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/SMART-EDUCATION-MODEL.git
cd SMART-EDUCATION-MODEL
```

### 2️⃣ Create Virtual Environment
```
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ pip install -r requirements.txt
```
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```
cd backend
python app.py
```
### 5️⃣ App will run at:
```
http://127.0.0.1:5000
```

## 📂 CSV Upload Format

### Your CSV file must contain these columns:
```
student_id,name,attendance,avg_marks,assignment_completion,behavior_score
```
### Example:
```
S001,John Doe,85,78,90,80
```

## 🔐 Authentication Flow
### 1.Select Role (Teacher / Student)

### 2.Signup (One-time)

### 3.Login

### 4.Access role-based dashboard

## 📊 Risk Logic
```
Average Score = (Attendance + Marks + Assignments + Behavior) / 4

≥ 75  → Low Risk
50–74 → Medium Risk
< 50  → High Risk
```

## DataSet Used to train the ML Model
https://www.kaggle.com/datasets/spscientist/students-performance-in-exams?

### we have used this kaggle DataSet to train our model by feature engineering with Ml-rule based logic

## 🌐 Free Deployment Options
```
You can deploy this project for free using:

Render

Railway

PythonAnywhere

SQLite works out-of-the-box for demo & hackathon usage.

```

## 🧪 Sample Credentials (After Signup)
### 1. Teacher → Upload CSV & view all students

## sample_csv:
```
student_id,name,attendance,avg_marks,assignment_completion,behavior_score
S002,rahul,80,56,60,7
```



### 2. Student → View personal dashboard using Student ID


##  🤝 Contributing
Contributions are welcome!

Fork the repo

Create a new branch

Commit changes

Open a Pull Request

## 📊 Can Improve to existing project

- Passwords not hashed
- SQLite instead of production DB
- Mobile responsiveness
- More interactive charts


## 🚀 Future Enhancements

While the current version of the Smart Education Model provides a complete and functional prototype, the following enhancements can be implemented in future iterations to improve scalability, security, and real-world usability:

1️⃣ **Advanced Machine Learning Integration**  
- Replace rule-based risk calculation with a trained ML model for more accurate predictions  
- Use historical student data to improve risk classification  
- Add model retraining support for new datasets  

2️⃣ **Improved Authentication & Security**  
- Implement password hashing using `bcrypt`  
- Add email verification and password recovery  
- Introduce role-based access decorators for better security  

3️⃣ **Database & Scalability Improvements**  
- Migrate from SQLite to PostgreSQL or MySQL for production use  
- Add database indexing for faster queries  
- Support multi-class and multi-teacher environments  

4️⃣ **Enhanced Analytics & Visualization**  
- Add interactive charts using Chart.js or Plotly  
- Provide downloadable student performance reports (PDF)  
- Track student progress trends over time  

5️⃣ **User Experience & Feature Expansion**  
- Add admin dashboard for managing users and data  
- Enable bulk student management and filtering  
- Integrate notifications for high-risk students  
- Make the UI fully responsive for mobile devices  

6️⃣ **Integrate this Analytical System**
- Can Integrate in existing platforms like moodle,google classroom
---

🔮 These enhancements will help transform the project from a prototype into a **production-ready smart education analytics platform**.


## 📜 License
This project is for educational and hackathon purposes.

## 👨‍💻 Author
Priyam Mondal


## If anyone read upto these

StudentsPerformance.csv file is used for training the model
Feature Engineer that data 

Feel free to fork and can also improve
