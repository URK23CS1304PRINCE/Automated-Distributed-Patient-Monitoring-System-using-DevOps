def check_alert(vitals):
    if vitals["heart_rate"] > 110:
        return "High Heart Rate!"
    if vitals["spo2"] < 90:
        return "Low Oxygen Level!"
    return None