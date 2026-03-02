from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
def init_db():
    conn=sqlite3.connect("employees.db")
    cursor=conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS employees(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   email VARCHAR2,
                   department TEXT
                   )
                   """)
    conn.commit()
    conn.close()
init_db()
# employees = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    email = request.form.get("email")
    department = request.form.get("department")
    conn=sqlite3.connect("employees.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO employees(name,email,department) VALUES (?,?,?)",
                      (name,email,department))
    conn.commit()
    conn.close()

    # employees.append({
    #     "name": name,
    #     "email": email,
    #     "department": department
    # })

    return redirect(url_for("view"))
@app.route("/view")
def view():
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, department FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template("view.html", employees=employees)




@app.route("/delete/<int:emp_id>")
def delete(emp_id):
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("view"))

if __name__ == "__main__":
    app.run(debug=True)