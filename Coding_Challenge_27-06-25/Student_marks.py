import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="sunnybunny.123", 
    database="schooldb"
)
cursor = conn.cursor()

print("\n--- All Records ---")
cursor.execute("SELECT * FROM studentscores")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT AVG(student_marks) FROM studentscores")
avg = cursor.fetchone()[0]
print(f"\nAverage Marks: {avg:.2f}")

print("\n--- Students Scoring Less Than 40 ---")
cursor.execute("SELECT student_name, student_subject, student_marks FROM studentscores WHERE student_marks < 40")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
