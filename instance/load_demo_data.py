import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "MediSync.db"

conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# ----------------------------
# 1️⃣ Load Patients
# ----------------------------
patients = pd.read_csv("patients.csv")

for _, row in patients.iterrows():
    cursor.execute("""
        INSERT INTO patient
        (id, name, email, password, phone, gender, age, blood_group, address, medical_history)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(row["id"]),
        row["name"],
        row["email"],
        row["password"],
        row["phone"],
        row["gender"],
        int(row["age"]),
        row["blood_group"],
        row["address"],
        row["medical_history"]
    ))

print("✅ Patients loaded")

# ----------------------------
# 2️⃣ Load Doctors
# ----------------------------
doctors = pd.read_csv("doctors.csv")

for _, row in doctors.iterrows():
    cursor.execute("""
        INSERT INTO doctor
        (id, name, email, password, phone, specialization, qualification, experience_years)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(row["id"]),
        row["name"],
        row["email"],
        row["password"],
        row["phone"],
        row["specialization"],
        row["qualification"],
        int(row["experience_years"])
    ))

print("✅ Doctors loaded")

# ----------------------------
# 3️⃣ Load Availability
# ----------------------------
availability = pd.read_csv("availability.csv")

for _, row in availability.iterrows():
    cursor.execute("""
        INSERT INTO availability
        (id, doctor_id, day, start_time, end_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        int(row["id"]),
        int(row["doctor_id"]),
        row["day"],
        row["start_time"],
        row["end_time"]
    ))

print("✅ Availability loaded")

# ----------------------------
# 4️⃣ Load Appointments
# ----------------------------
appointments = pd.read_csv("appointments.csv")

for _, row in appointments.iterrows():
    cursor.execute("""
        INSERT INTO appointment
        (id, doctor_id, patient_id, status, date, time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(row["id"]),
        int(row["doctor_id"]),
        int(row["patient_id"]),
        row["status"],
        row["date"],
        row["time"]
    ))

print("✅ Appointments loaded")

conn.commit()
conn.close()

print("\n🎉 All demo data loaded successfully!")