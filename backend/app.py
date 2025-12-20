from flask import Flask, render_template, request, redirect, session, flash, jsonify
import sqlite3, csv, io

app = Flask(__name__)
app.secret_key = "secret123"
DB = "database.db"

# ---------- DB ----------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        student_id TEXT
    )
    """)

    cur.execute("""
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

    conn.commit()
    conn.close()

# ---------- RISK ----------
def calculate_risk(a, m, ass, b):
    score = (a + m + ass + b) / 4
    if score >= 75:
        return "Low"
    elif score >= 50:
        return "Medium"
    return "High"

# ---------- ROLE ----------
@app.route("/")
def role_select():
    return render_template("role_select.html")

@app.route("/select_role", methods=["POST"])
def select_role():
    session["role"] = request.form["role"]
    return redirect(f"/login/{session['role']}")

# ---------- LOGIN ----------
@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (u, p, role)
        ).fetchone()
        conn.close()

        if user:
            session["role"] = role
            session["student_id"] = user["student_id"]
            return redirect("/teacher" if role == "teacher" else "/student")

        flash("Invalid credentials")

    return render_template("login.html", role=role)

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- TEACHER ----------
@app.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect("/")

    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("teacher_dashboard.html", students=students)

# ---------- UPLOAD ----------
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if session.get("role") != "teacher":
        return jsonify({"error": "Unauthorized"}), 403

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    stream = io.StringIO(file.stream.read().decode("utf8"))
    reader = csv.DictReader(stream)

    conn = get_db()
    cur = conn.cursor()

    for r in reader:
        a = float(r["attendance"])
        m = float(r["avg_marks"])
        ass = float(r["assignment_completion"])
        b = float(r["behavior_score"])

        risk = calculate_risk(a, m, ass, b)

        cur.execute("""
        INSERT OR REPLACE INTO students
        VALUES (?,?,?,?,?,?,?)
        """, (r["student_id"], r["name"], a, m, ass, b, risk))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

# ---------- STUDENT ----------
@app.route("/student")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/")

    conn = get_db()
    s = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (session["student_id"],)
    ).fetchone()
    conn.close()

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

# ---------- STUDENT REPORT ----------
@app.route("/student_report/<student_id>")
def student_report(student_id):
    if session.get("role") != "teacher":
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    ).fetchone()
    conn.close()

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

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

