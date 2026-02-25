import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta

# ======================================================
# CONFIG
# ======================================================
DB_FILE = "MediSync.db"

conn = sqlite3.connect(DB_FILE)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

# ======================================================
# LOAD EXISTING DATA
# ======================================================
doctors = pd.read_sql_query("SELECT * FROM doctor", conn)
patients = pd.read_sql_query("SELECT * FROM patient", conn)
availability = pd.read_sql_query("SELECT * FROM availability", conn)
appointments = pd.read_sql_query("SELECT * FROM appointment", conn)

existing_patient_ids = set(int(x) for x in patients["id"])

# ======================================================
# 1️⃣ ADD 20 NEW DOCTORS (UNEQUAL DISTRIBUTION)
# ======================================================

specialization_distribution = [
    ("Family Medicine/General Practitioner", 5),
    ("Internal Medicine", 3),
    ("Pediatrics", 3),
    ("Cardiology", 2),
    ("Emergency Medicine", 2),
    ("Dermatology", 2),
    ("Orthopedic Surgery", 1),
    ("Gastroenterology", 1),
    ("Psychiatry", 1)
]

new_doctors = []
new_availability = []

max_doc = cursor.execute("SELECT MAX(id) FROM doctor").fetchone()[0]
next_doctor_id = 1 if max_doc is None else int(max_doc) + 1

max_avail = cursor.execute("SELECT MAX(id) FROM availability").fetchone()[0]
next_avail_id = 1 if max_avail is None else int(max_avail) + 1

for spec, count in specialization_distribution:
    for _ in range(count):

        did = int(next_doctor_id)
        name = f"Doctor{did}"

        new_doctors.append((
            int(did),
            str(name),
            str(f"dr.{name.lower()}_{did}_appointed@gmail.com"),
            str(f"dr{name.lower()}@{did}"),
            str("9" + "".join(str(random.randint(0,9)) for _ in range(9))),
            str(spec),
            str("MBBS, MD"),
            int(random.randint(5, 20))
        ))

        # Weekly availability (3 weekdays)
        for day in random.sample(
            ["Monday","Tuesday","Wednesday","Thursday","Friday"], 3):

            start_hour = random.randint(9, 12)
            end_hour = start_hour + 4

            new_availability.append((
                int(next_avail_id),
                int(did),
                str(day),
                str(f"{start_hour:02d}:00:00"),
                str(f"{end_hour:02d}:00:00")
            ))

            next_avail_id += 1

        next_doctor_id += 1

cursor.executemany("""
INSERT INTO doctor
(id, name, email, password, phone, specialization, qualification, experience_years)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", new_doctors)

cursor.executemany("""
INSERT INTO availability
(id, doctor_id, day, start_time, end_time)
VALUES (?, ?, ?, ?, ?)
""", new_availability)

print("✅ 20 doctors added")

# ======================================================
# 2️⃣ ADD 300 UNEVEN APPOINTMENTS
# ======================================================

doctors = pd.read_sql_query("SELECT * FROM doctor", conn)
availability = pd.read_sql_query("SELECT * FROM availability", conn)
appointments = pd.read_sql_query("SELECT * FROM appointment", conn)

doctor_specialization = {
    int(row["id"]): row["specialization"]
    for _, row in doctors.iterrows()
}

demand_weights = {
    "Family Medicine/General Practitioner": 25,
    "Internal Medicine": 15,
    "Pediatrics": 15,
    "Emergency Medicine": 12,
    "Cardiology": 10,
    "Orthopedic Surgery": 8,
    "Dermatology": 8,
    "Psychiatry": 5,
    "Gastroenterology": 2,
    "Oncology": 1,
    "Endocrinology": 1
}

weighted_doctors = []
for did, spec in doctor_specialization.items():
    weight = demand_weights.get(spec, 1)
    weighted_doctors.extend([int(did)] * int(weight))

existing_slots = set(
    (int(row["doctor_id"]), row["date"], row["time"])
    for _, row in appointments.iterrows()
)

max_app = cursor.execute("SELECT MAX(id) FROM appointment").fetchone()[0]
next_app_id = 1 if max_app is None else int(max_app) + 1

new_appointments = []
start_date = datetime.today() - timedelta(days=60)

while len(new_appointments) < 300:

    doctor_id = int(random.choice(weighted_doctors))
    patient_id = int(random.choice(list(existing_patient_ids)))

    doc_avail = availability[availability["doctor_id"] == doctor_id]
    if doc_avail.empty:
        continue

    row = doc_avail.sample(1).iloc[0]
    day = row["day"]

    start_hour = int(row["start_time"].split(":")[0])
    end_hour = int(row["end_time"].split(":")[0])

    slot_hour = random.randint(start_hour, end_hour - 1)
    slot_min = random.choice([0,20,40])
    slot_time = f"{slot_hour:02d}:{slot_min:02d}:00"

    rand_days = random.randint(0,120)
    app_date = start_date + timedelta(days=rand_days)

    if app_date.strftime("%A") != day:
        continue

    date_str = app_date.strftime("%Y-%m-%d")
    slot_key = (doctor_id, date_str, slot_time)

    if slot_key in existing_slots:
        continue

    spec = doctor_specialization[doctor_id]

    if spec == "Dermatology":
        status = random.choices(
            ["cancelled","completed","booked"],
            weights=[60,20,20]
        )[0]
    else:
        status = random.choices(
            ["completed","booked","cancelled"],
            weights=[60,30,10]
        )[0]

    new_appointments.append((
        int(next_app_id),
        int(doctor_id),
        int(patient_id),
        str(status),
        str(date_str),
        str(slot_time)
    ))

    existing_slots.add(slot_key)
    next_app_id += 1

cursor.executemany("""
INSERT INTO appointment
(id, doctor_id, patient_id, status, date, time)
VALUES (?, ?, ?, ?, ?, ?)
""", new_appointments)

print("✅ 300 appointments added")

# ======================================================
# 3️⃣ ADD 450+ TREATMENTS
# ======================================================

appointments = pd.read_sql_query("SELECT * FROM appointment", conn)

completed = appointments[appointments["status"] == "completed"]

existing_treatments = pd.read_sql_query(
    "SELECT appointment_id FROM treatment", conn)

treated_ids = set(int(x) for x in existing_treatments["appointment_id"])

eligible = [
    row for _, row in completed.iterrows()
    if int(row["id"]) not in treated_ids
]

random.shuffle(eligible)
eligible = eligible[:450]

max_treat = cursor.execute("SELECT MAX(id) FROM treatment").fetchone()[0]
next_treat_id = 1 if max_treat is None else int(max_treat) + 1

new_treatments = []

for row in eligible:
    new_treatments.append((
        int(next_treat_id),
        int(row["id"]),
        "General Diagnosis",
        "Standard Prescription",
        "Follow-up in 2 weeks"
    ))
    next_treat_id += 1

cursor.executemany("""
INSERT INTO treatment
(id, appointment_id, diagnosis, prescription, notes)
VALUES (?, ?, ?, ?, ?)
""", new_treatments)

print("✅ Treatments added")

# ======================================================
# COMMIT
# ======================================================

conn.commit()
conn.close()

print("\n🎉 Data augmentation completed successfully!")