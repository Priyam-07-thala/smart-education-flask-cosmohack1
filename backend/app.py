from flask import Flask, render_template, request, redirect, session, flash, jsonify
import sqlite3, csv, io, os
from werkzeug.security import generate_password_hash, check_password_hash

# =============================
# APP SETUP
# =============================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_fallback_key")
DB = "database.db"


# =============================
# DATABASE HELPERS
# =============================
def get_db():
    conn = sqlite3.connect(
        DB,
        timeout=10,
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("PRAGMA journal_mode=WAL;")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            student_id TEXT
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT,
            attendance REAL,
            avg_marks REAL,
            assignment_completion REAL,
            behavior_score REAL,
            risk TEXT
        )
        """)


# =============================
# IMPORT ML + GEMINI
# =============================
from backend.ml.train_model import predict_risk
from backend.ml.prompt_builder import build_gemini_prompt
from backend.ml.gemini_client import generate_explanation


# =============================
# ROLE SELECTION
# =============================
@app.route("/")
def role_select():
    return render_template("role_select.html")


@app.route("/select_role", methods=["POST"])
def select_role():
    session["role"] = request.form["role"]
    return redirect(f"/login/{session['role']}")


# =============================
# LOGIN
# =============================
@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username=? AND role=?",
                (u, role)
            ).fetchone()

        if user and check_password_hash(user["password"], p):
            session["role"] = role
            session["student_id"] = user["student_id"]
            return redirect("/teacher" if role == "teacher" else "/student")

        flash("Invalid credentials")

    return render_template("login.html", role=role)


# =============================
# LOGOUT
# =============================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =============================
# SIGNUP
# =============================
@app.route("/signup/<role>", methods=["GET", "POST"])
def signup(role):
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        sid = request.form.get("student_id")

        hashed = generate_password_hash(p)

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO users (username, password, role, student_id) VALUES (?, ?, ?, ?)",
                    (u, hashed, role, sid if role == "student" else None)
                )

            flash("Signup successful. Please login.")
            return redirect(f"/login/{role}")

        except sqlite3.IntegrityError:
            flash("Username already exists")

    return render_template("signup.html", role=role)


# =============================
# TEACHER DASHBOARD
# =============================
@app.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect("/")

    with get_db() as conn:
        students = conn.execute("SELECT * FROM students").fetchall()

    return render_template("teacher_dashboard.html", students=students)


# =============================
# CSV UPLOAD  ✅ FULLY FIXED
# =============================
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if session.get("role") != "teacher":
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8", errors="ignore"))
        reader = csv.DictReader(stream)

        required_fields = [
            "student_id", "name",
            "attendance", "avg_marks",
            "assignment_completion", "behavior_score"
        ]

        with get_db() as conn:
            cur = conn.cursor()

            for r in reader:
                if not all(field in r and r[field] for field in required_fields):
                    continue

                a = float(r["attendance"].strip())
                m = float(r["avg_marks"].strip())
                ass = float(r["assignment_completion"].strip())
                b = float(r["behavior_score"].strip())

                student_data = {
                    "attendance": a,
                    "marks": m,
                    "assignments": ass,
                    "behavior": b
                }

                # ✅ SAFE ML CALL
                try:
                    risk = predict_risk(student_data)
                except Exception as e:
                    print("ML error, using fallback:", e)
                    avg = (a + m + ass + b * 10) / 4
                    if avg >= 75:
                        risk = "Low"
                    elif avg >= 50:
                        risk = "Medium"
                    else:
                        risk = "High"

                cur.execute("""
                INSERT OR REPLACE INTO students
                VALUES (?,?,?,?,?,?,?)
                """, (r["student_id"], r["name"], a, m, ass, b, risk))

        return jsonify({"success": True})

    except Exception as e:
        print("CSV upload error:", e)
        return jsonify({
            "success": False,
            "error": "Server error while processing CSV"
        }), 500



# =============================
# STUDENT DASHBOARD
# =============================
@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/")

    with get_db() as conn:
        s = conn.execute(
            "SELECT * FROM students WHERE student_id=?",
            (session["student_id"],)
        ).fetchone()

    if not s:
        flash("Performance data not uploaded yet.")
        return render_template("student_dashboard.html", student=None)

    chart_data = {
        "attendance": s["attendance"],
        "marks": s["avg_marks"],
        "assignments": s["assignment_completion"],
        "behavior": s["behavior_score"]
    }

    return render_template(
        "student_dashboard.html",
        student=s,
        chart_data=chart_data,
        risk=s["risk"]
    )


# =============================
# STUDENT REPORT
# =============================
@app.route("/student_report/<student_id>")
def student_report(student_id):
    if session.get("role") != "teacher":
        return redirect("/")

    with get_db() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        ).fetchone()

    if not student:
        flash("Student not found")
        return redirect("/teacher")

    chart_data = {
        "attendance": student["attendance"],
        "marks": student["avg_marks"],
        "assignments": student["assignment_completion"],
        "behavior": student["behavior_score"]
    }

    return render_template(
        "student_report.html",
        student=student,
        chart_data=chart_data,
        risk=student["risk"]
    )


# =============================
# EXPLAINABLE AI
# =============================
@app.route("/explain/<student_id>")
def explain_student(student_id):
    if session.get("role") != "teacher":
        return jsonify({"success": False}), 403

    with get_db() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        ).fetchone()

    if not student:
        return jsonify({"success": False}), 404

    student_data = {
        "attendance": student["attendance"],
        "marks": student["avg_marks"],
        "assignments": student["assignment_completion"],
        "behavior": student["behavior_score"]
    }

    risk = student["risk"]

    explanation = generate_explanation(student_data, risk)
    return jsonify(explanation)


    # ✅ USE STORED RISK (NO ML CALL)
    risk = student["risk"]

    prompt = build_gemini_prompt(student_data, risk)
    explanation = generate_explanation(prompt)

    return jsonify({
        "success": True,
        **explanation
    })


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    init_db()
    app.run(debug=True, use_reloader=False)
