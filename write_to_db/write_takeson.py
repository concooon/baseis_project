import sqlite3
import random

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

# Get existing Project Pnos and Department Dnos
project_pnos = cursor.execute("SELECT Project_number FROM PROJECT").fetchall()
department_dnos = cursor.execute("SELECT Dnumber FROM DEPARTMENT").fetchall()

# Generate and insert data into the "Take_on" table
for project_number in project_pnos:
    pno = project_number[0]
    dno = random.choice(department_dnos)[0]

    cursor.execute('''
        INSERT INTO "Take_on" (
            "Pno",
            "Dno"
        ) VALUES (?, ?)
    ''', (pno, dno))

# Commit changes and close connection
conn.commit()
conn.close()
