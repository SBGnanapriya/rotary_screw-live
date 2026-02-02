import time
import random
import pandas as pd
import joblib

# Load trained model
model = joblib.load("compressor_fault_model.pkl")

status_map = {0: "NORMAL", 1: "WARNING", 2: "CRITICAL"}

# ---------------- STATUS FUNCTIONS ----------------

def current_status(current):
    if current < 10:
        return "CRITICAL"
    elif 25 <= current <= 60:
        return "NORMAL"
    elif 60 < current <= 70:
        return "WARNING"
    else:
        return "CRITICAL"

def temperature_status(temp):
    if 60 <= temp <= 90:
        return "NORMAL"
    elif temp <= 105:
        return "WARNING"
    else:
        return "CRITICAL"

def pressure_status(pressure):
    if 2.8 <= pressure <= 3.2:
        return "NORMAL"
    elif 2.4 <= pressure <= 3.6:
        return "WARNING"
    else:
        return "CRITICAL"

def vibration_status(vib):
    if vib <= 4:
        return "NORMAL"
    elif vib <= 7:
        return "WARNING"
    else:
        return "CRITICAL"

def dp_status(dp):
    if dp <= 0.2:
        return "NORMAL"
    elif dp <= 0.5:
        return "WARNING"
    else:
        return "CRITICAL"

def diagnose_fault(current, temp, pressure, vib, dp):
    if current > 60 and pressure < 2.8:
        return "Air leakage"
    elif vib > 4 and current > 60:
        return "Bearing / alignment issue"
    elif dp > 0.5:
        return "Filter choked"
    elif temp > 90 and dp > 0.2:
        return "Cooling / filter issue"
    else:
        return "No specific fault detected"

# ---------------- LIVE DATA GENERATOR ----------------

def generate_live_data(run_hours):
    return {
        "current": round(random.uniform(45, 80), 2),
        "temperature": round(random.uniform(65, 110), 2),
        "pressure": round(random.uniform(2.5, 3.5), 2),
        "vibration": round(random.uniform(2, 9), 2),
        "dp_filter": round(random.uniform(0.1, 0.7), 2),
        "run_hours": run_hours
    }

# ---------------- LIVE MONITORING LOOP ----------------

run_hours = 1500

print("\n🔴 LIVE COMPRESSOR CONDITION MONITORING STARTED 🔴\n")

while True:
    data = generate_live_data(run_hours)
    run_hours += 1

    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]

    print("==============================================")
    print(" LIVE DIAGNOSTIC REPORT")
    print("==============================================")
    print(f"Motor Current     : {data['current']} A → {current_status(data['current'])}")
    print(f"Temperature       : {data['temperature']} °C → {temperature_status(data['temperature'])}")
    print(f"Line Pressure     : {data['pressure']} bar → {pressure_status(data['pressure'])}")
    print(f"Vibration         : {data['vibration']} mm/s → {vibration_status(data['vibration'])}")
    print(f"Filter ΔP         : {data['dp_filter']} bar → {dp_status(data['dp_filter'])}")
    print(f"Running Hours     : {data['run_hours']} hrs")
    print("----------------------------------------------")
    print(f"OVERALL STATUS    : {status_map[prediction]}")
    print(f"LIKELY FAULT      : {diagnose_fault(**data)}")
    print("==============================================\n")

    if status_map[prediction] == "CRITICAL":
        print("🚨 ALERT: CRITICAL CONDITION DETECTED 🚨\n")

    time.sleep(5)  # simulate live update every 5 seconds
