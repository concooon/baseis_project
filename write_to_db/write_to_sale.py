import sqlite3
import random

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

# Get existing Book ISBNs and Sale Ids
book_ids = cursor.execute("SELECT ISBN FROM BOOK").fetchall()
sale_ids = cursor.execute("SELECT Id FROM SALE").fetchall()

# Generate and insert data into the "TO_SALE" table
for _ in range(30):  # Generate 150 entries
    book_id = random.choice(book_ids)[0]
    sale_id = random.choice(sale_ids)[0]
    quantity = random.randint(1, 10)  # Adjust the range according to your needs

    try:
        cursor.execute('''
            INSERT INTO "TO_SALE" (
                "Book_id",
                "Sale_id",
                "Quantity"
            ) VALUES (?, ?, ?)
        ''', (book_id, sale_id, quantity))
    except sqlite3.IntegrityError:
        # Handle the case where a duplicate Sale_id is encountered
        pass

# Commit changes and close connection
conn.commit()
conn.close()
