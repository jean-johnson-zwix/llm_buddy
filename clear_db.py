import sqlite3

conn = sqlite3.connect("data/benchmarks.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM results")
cursor.execute("DELETE FROM runs")

conn.commit()
conn.close()

print("Database cleared. All test data removed.")