import sqlite3
import random
from faker import Faker

fake = Faker('el_GR')  # Greek language setting for Faker

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

# Get existing AFMs and Pnos
freelancer_afms = cursor.execute("SELECT AFM FROM FREELANCER").fetchall()
project_pnos = cursor.execute("SELECT Project_number FROM PROJECT").fetchall()

# Function to generate random notes
def random_notes():
    return fake.text(max_nb_chars=250)

# Generate and insert data into the "COOPERATES" table
for _ in range(50):  # Generate 50 entries
    afm = random.choice(freelancer_afms)[0]
    pno = random.choice(project_pnos)[0]
    payment = random.randint(100, 10000)
    notes = random_notes()

    cursor.execute('''
        INSERT INTO "COOPERATES" (
            "AFM",
            "Pno",
            "Payment",
            "Notes"
        ) VALUES (?, ?, ?, ?)
    ''', (afm, pno, payment, notes))

# Commit changes and close connection
conn.commit()
conn.close()
