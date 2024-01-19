import sqlite3
import random

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

# Get existing Employee AFMs and Project Pnos
employee_afms = cursor.execute("SELECT AFM FROM EMPLOYEE").fetchall()
project_pnos = cursor.execute("SELECT Project_number FROM PROJECT").fetchall()

# Generate and insert data into the "Works_on" table
for _ in range(100):  # Generate 100 entries
    emp_afm = random.choice(employee_afms)[0]
    pno = random.choice(project_pnos)[0]
    hours = random.randint(10, 80)  # Adjust the range according to your needs

    cursor.execute('''
        INSERT INTO "Works_on" (
            "Emp_AFM",
            "Pno",
            "Hours"
        ) VALUES (?, ?, ?)
    ''', (emp_afm, pno, hours))

# Commit changes and close connection
conn.commit()
conn.close()
