import sqlite3
import random
from faker import Faker

fake = Faker('el_GR')  # Greek language setting for Faker

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

# Get existing Customer Ids
customer_ids = cursor.execute("SELECT AFM FROM CUSTOMER").fetchall()

# Function to generate random dates in the format 'yyyy-mm-dd'
def random_date():
    return fake.date_of_birth(minimum_age=1, maximum_age=10).strftime('%Y-%m-%d')

# Generate and insert data into the "SALE" table
for sale_id in range(1, 51):  # Generate 50 entries
    sale_date = random_date()
    subtotal = round(random.uniform(50, 500), 2)
    discount = random.randint(0, 20)
    total = round(subtotal * (1 - discount / 100), 2)
    customer_id = random.choice(customer_ids)[0]

    cursor.execute('''
        INSERT INTO "SALE" (
            "Id",
            "Date",
            "Subtotal",
            "Discount",
            "Total",
            "Customer_Id"
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (sale_id, sale_date, subtotal, discount, total, customer_id))

# Commit changes and close connection
conn.commit()
conn.close()
