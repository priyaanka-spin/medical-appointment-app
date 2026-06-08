from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return """
    <h1>Medical Appointment Booking - Version 2</h1>

    <form action="/book" method="post">
      Name:<br>
      <input type="text" name="name"><br><br>

      Date:<br>
      <input type="date" name="date"><br><br>

      <input type="submit" value="Book Appointment">
    </form>
    """

@app.route("/book", methods=["POST"])
def book():
    name = request.form["name"]
    date = request.form["date"]

    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO appointments(name,date) VALUES (?,?)",
        (name,date)
    )

    conn.commit()
    conn.close()

    return f"""
    <h2>Appointment Saved</h2>
    Name: {name}<br>
    Date: {date}
    """
@app.route("/view")
def view():

    conn = sqlite3.connect("appointments.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM appointments")
    rows = cur.fetchall()

    conn.close()

    result = "<h1>All Appointments</h1>"

    for row in rows:
        result += f"<p>ID:{row[0]} | Name:{row[1]} | Date:{row[2]}</p>"

    return result
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
