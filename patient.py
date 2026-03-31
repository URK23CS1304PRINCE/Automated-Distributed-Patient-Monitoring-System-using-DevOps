import socket
import time
import random
import sys
from utils import format_data

SERVER_IP = "127.0.0.1"
PORT = 9999

# 🔹 Generate random vitals
def generate_vitals():
    return {
        "heart_rate": random.randint(60, 120),
        "temperature": round(random.uniform(36.0, 39.5), 1),
        "spo2": random.randint(85, 100)
    }

# 🔹 Adaptive Monitoring Logic (NOVELTY 🔥)
def get_condition(v):
    if v["heart_rate"] > 110 or v["spo2"] < 90:
        return "CRITICAL", 1   # send every 1 sec
    elif v["heart_rate"] > 95 or v["temperature"] > 38:
        return "WARNING", 3    # send every 3 sec
    else:
        return "STABLE", 5     # send every 5 sec

# 🔹 Main Patient Process
def run_patient(patient_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    print(f"🟢 Patient {patient_id} started...")

    while True:
        vitals = generate_vitals()
        state, freq = get_condition(vitals)

        # ✅ Using utils (structured JSON)
        message = format_data(patient_id, vitals, state)
        client.send(message.encode())

        print(f"[Patient {patient_id}] {vitals} → {state} (freq={freq}s)")

        time.sleep(freq)

# 🔹 Run with command line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python patient.py <patient_id>")
        sys.exit()

    pid = int(sys.argv[1])
    run_patient(pid)