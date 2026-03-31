import json

def format_data(patient_id, vitals, state):
    data = {
        "patient_id": patient_id,
        "heart_rate": vitals["heart_rate"],
        "temperature": vitals["temperature"],
        "spo2": vitals["spo2"],
        "state": state
    }
    return json.dumps(data)