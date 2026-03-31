from flask import Flask, render_template, request, redirect, session, jsonify
import random
import time
import threading
import os

app = Flask(__name__)
app.secret_key = "secret123"

latest_data = []

def simulate_patients():
    global latest_data
    while True:
        new_data = []
        for i in range(1, 11):
            heart = random.randint(60, 130)
            temp = round(random.uniform(36.0, 39.5), 1)
            spo2 = random.randint(85, 100)

            if heart > 110 or spo2 < 90:
                state = "CRITICAL"
            elif heart > 95 or temp > 38:
                state = "WARNING"
            else:
                state = "STABLE"

            new_data.append({
                "patient_id": i,
                "heart_rate": heart,
                "temperature": temp,
                "spo2": spo2,
                "state": state
            })

        latest_data = new_data
        time.sleep(3)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/")
        return "Invalid"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", data=latest_data)

@app.route("/data")
def data():
    return jsonify({"patients": latest_data})

if __name__ == "__main__":
    threading.Thread(target=simulate_patients, daemon=True).start()
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
