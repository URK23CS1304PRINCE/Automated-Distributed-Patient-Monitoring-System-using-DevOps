from flask import Flask, render_template, request, redirect, session, jsonify
import socket
import threading
import json
import os
import random
import time

app = Flask(__name__)
app.secret_key = "secret123"

# 🔐 FORCE LOGIN FOR ALL ROUTES
@app.before_request
def require_login():
    allowed_routes = ["login", "static"]

    if request.endpoint not in allowed_routes and "user" not in session:
        return redirect("/login")


# 🔹 Initial sample data
latest_data = [
    {"patient_id": 1, "heart_rate": 80, "temperature": 37.0, "spo2": 98, "state": "STABLE"},
    {"patient_id": 2, "heart_rate": 110, "temperature": 38.5, "spo2": 92, "state": "WARNING"},
    {"patient_id": 3, "heart_rate": 120, "temperature": 39.0, "spo2": 88, "state": "CRITICAL"}
]

# 🔹 SOCKET SERVER (LOCAL DISTRIBUTED SYSTEM)
def socket_server():
    HOST = "0.0.0.0"
    PORT = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("🟢 Socket Server Running...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


def handle_client(conn):
    global latest_data

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            data_dict = json.loads(data)

            latest_data.append(data_dict)
            latest_data = latest_data[-10:]

        except:
            break

    conn.close()


# 🔥 CLOUD AUTO-SIMULATION
def simulate_patients():
    global latest_data

    while True:
        new_data = []

        for i in range(1, 6):
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


# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return "<h3 style='color:red'>Invalid Credentials</h3>"

    return render_template("login.html")


# 🔐 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# 🏠 DASHBOARD
@app.route("/")
def index():
    return render_template("index.html", data=latest_data)


# 📊 API
@app.route("/data")
def data():
    return jsonify({"patients": latest_data})


# 🚀 MAIN
PORT = int(os.environ.get("PORT", 10000))

if os.environ.get("RENDER") is None:
    # 💻 LOCAL → REAL DISTRIBUTED SYSTEM
    threading.Thread(target=socket_server, daemon=True).start()
else:
    # 🌐 CLOUD → SIMULATION
    threading.Thread(target=simulate_patients, daemon=True).start()

app.run(host="0.0.0.0", port=PORT)
