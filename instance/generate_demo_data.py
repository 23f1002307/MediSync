import csv
import random
from datetime import datetime, timedelta, time

# -------------------------
# CONFIG
# -------------------------
NUM_DOCTORS = 40
NUM_PATIENTS = 150
NUM_APPOINTMENTS = 500
SLOT_MINUTES = 20

SPECIALIZATIONS = [
    "Family Medicine/General Practitioner",
    "Internal Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Obstetrics & Gynecology (OB/GYN)",
    "Orthopedic Surgery",
    "Gastroenterology",
    "Ophthalmology",
    "Psychiatry",
    "Otolaryngology (ENT)",
    "Endocrinology",
    "Urology",
    "Oncology",
    "Emergency Medicine"
]

WEEK_DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def random_phone():
    return "9" + "".join([str(random.randint(0,9)) for _ in range(9)])

def random_time_between(start_hour, end_hour):
    start = time(start_hour, 0)
    end = time(end_hour, 0)
    return start, end

# -------------------------
# 1️⃣ Generate Doctors
# -------------------------
doctors = []
for i in range(1, NUM_DOCTORS+1):
    first_name = f"Doctor{i}"
    specialization = SPECIALIZATIONS[(i-1) % len(SPECIALIZATIONS)]
    doctors.append([
        i,
        first_name,
        f"dr.{first_name.lower()}_{i}_appointed@gmail.com",
        f"dr{first_name.lower()}@{i}",
        random_phone(),
        specialization,
        "MBBS, MD",
        random.randint(3, 25)
    ])

with open("doctors.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id","name","email","password","phone","specialization","qualification","experience_years"])
    writer.writerows(doctors)

# -------------------------
# 2️⃣ Generate Patients
# -------------------------
patients = []
for i in range(1, NUM_PATIENTS+1):
    first_name = f"Patient{i}"
    patients.append([
        i,
        first_name,
        f"patient_{first_name.lower()}_{i}_appointed@gmail.com",
        f"patient_{first_name.lower()}@{i}",
        random_phone(),
        random.choice(["M","F"]),
        random.randint(18,75),
        random.choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"]),
        f"Address {i}",
        "None"
    ])

with open("patients.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id","name","email","password","phone","gender","age","blood_group","address","medical_history"])
    writer.writerows(patients)

# -------------------------
# 3️⃣ Generate Availability
# -------------------------
availability = []
availability_map = {}

avail_id = 1

for doctor in doctors:
    doctor_id = doctor[0]
    availability_map[doctor_id] = {}

    # each doctor available 3–5 random days
    days = random.sample(WEEK_DAYS, random.randint(3,5))

    for day in days:
        start_hour = random.randint(9, 14)
        end_hour = start_hour + random.randint(3,5)

        availability.append([
            avail_id,
            doctor_id,
            day,
            f"{start_hour:02d}:00:00",
            f"{end_hour:02d}:00:00"
        ])

        availability_map[doctor_id][day] = (start_hour, end_hour)
        avail_id += 1

with open("availability.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id","doctor_id","day","start_time","end_time"])
    writer.writerows(availability)

# -------------------------
# 4️⃣ Generate Appointments
# -------------------------
appointments = []
appointment_id = 1
booked_slots = set()

start_date = datetime.today() - timedelta(days=60)

while len(appointments) < NUM_APPOINTMENTS:
    doctor_id = random.randint(1, NUM_DOCTORS)
    patient_id = random.randint(1, NUM_PATIENTS)

    if not availability_map[doctor_id]:
        continue

    day = random.choice(list(availability_map[doctor_id].keys()))
    start_hour, end_hour = availability_map[doctor_id][day]

    # generate slot
    slot_hour = random.randint(start_hour, end_hour-1)
    slot_min = random.choice([0,20,40])
    slot_time = f"{slot_hour:02d}:{slot_min:02d}:00"

    # generate date matching weekday
    random_days_offset = random.randint(0,120)
    appointment_date = start_date + timedelta(days=random_days_offset)

    if appointment_date.strftime("%A") != day:
        continue

    slot_key = (doctor_id, appointment_date.strftime("%Y-%m-%d"), slot_time)

    if slot_key in booked_slots:
        continue

    booked_slots.add(slot_key)

    appointments.append([
        appointment_id,
        doctor_id,
        patient_id,
        random.choice(["booked","completed","cancelled"]),
        appointment_date.strftime("%Y-%m-%d"),
        slot_time
    ])

    appointment_id += 1

with open("appointments.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id","doctor_id","patient_id","status","date","time"])
    writer.writerows(appointments)

print("✅ CSV files generated successfully!")