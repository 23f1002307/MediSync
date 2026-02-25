import sqlite3
import pandas as pd

conn = sqlite3.connect("MediSync.db")

tables = ["patient","doctor","availability","appointment", "treatment"]

# Export
for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f"backup_{table}.csv", index=False)

# Clear tables
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = OFF;")

for table in ["appointment","availability","doctor","patient"]:
    cursor.execute(f"DELETE FROM {table};")

# cursor.execute("DELETE FROM sqlite_sequence;")
cursor.execute("PRAGMA foreign_keys = ON;")

conn.commit()
conn.close()

print("Backup complete and tables cleared safely.")