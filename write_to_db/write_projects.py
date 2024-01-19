import sqlite3
import random
from faker import Faker
from datetime import datetime

fake = Faker('el_GR')  # Greek language setting for Faker

# Create SQLite connection and cursor
conn = sqlite3.connect(r"C:\Users\Nestoras\Documents\db\baseis_project\pub.db")  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

cursor.execute('DELETE FROM PROJECT')

# Generate and insert data into the "PROJECT" table
for project_number in range(1, 201):
    title = fake.text(max_nb_chars=80)
    description = fake.text(max_nb_chars=300)
    project_type = random.choices(['Διαφημιστική Καμπάνια', 'Έκδοση Βιβλίου', 'Προώθηση', 'Επανέκδοση', 'Μετάφραση', 'Άλλο'], weights=[1, 7, 2, 2, 3, 4])[0]
    start_date = fake.date_this_decade().strftime('%Y-%m-%d')
    end_date = fake.date_between(start_date=datetime.strptime(start_date, '%Y-%m-%d').date(), end_date='+90d').strftime('%Y-%m-%d')
    
    # Ensure real_end_date is not before real_start_date
    real_start_date = fake.date_this_decade().strftime('%Y-%m-%d')
    real_end_date = fake.date_between(start_date=datetime.strptime(real_start_date, '%Y-%m-%d').date(), end_date='+90d').strftime('%Y-%m-%d')

    # Random choice for the "State" field
    state_choices = ['Σε εξέλιξη', 'Σε παύση', 'Προγραμματισμένο', 'Ολοκληρωμένο', 'Ακυρωμένο']
    state = random.choice(state_choices)
    
    # Biased choice for more "Έκδοση Βιβλίου"
    if project_type == 'Έκδοση Βιβλίου' and random.random() < 0.6:
        real_end_date = '--'  # Set the end_date to '--' for ongoing projects
        state = 'Σε εξέλιξη'

    cursor.execute('''
        INSERT INTO "PROJECT" (
            "Project_number",
            "Title",
            "Description",
            "Type",
            "Start_date",
            "End_date",
            "Real_start_date",
            "Real_end_date",
            "Budget",
            "State"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (project_number, title, description, project_type, start_date, end_date, real_start_date, real_end_date, random.randint(1000, 10000), state))

# Commit changes and close connection
conn.commit()
conn.close()
