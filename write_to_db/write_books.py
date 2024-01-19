import sqlite3
from faker import Faker

fake = Faker('el_GR')  # Greek language setting for Faker

# Create SQLite connection and cursor
conn = sqlite3.connect('database3.db')  # Replace 'your_database.db' with your database file
cursor = conn.cursor()

projects = cursor.execute("SELECT Project_number from PROJECT where type = 'Έκδοση Βιβλίου' or type = 'Επανέκδοση' or type='Μετάφραση';").fetchall()
cursor.execute('DELETE FROM BOOK;')

print(projects)

# List of book titles in various languages

def get_title(language):
    if language == 'Ελληνικά':
        return fake.sentence(nb_words=fake.random_int(min=1, max=4), variable_nb_words=True, ext_word_list=None)
    else:
        return fake.catch_phrase()


# Languages for books
languages = ['Ελληνικά', 'Αγγλικά'] #, 'Γαλλικά', 'Γερμανικά', 'Ισπανικά', 'Ιταλικά', 'Πορτογαλικά', 'Ρωσικά', 'Κινεζικά']

# Generate and insert data into the "BOOK" table
for project_number in projects:
    isbn = fake.isbn13()
    author = fake.name()
    language = fake.random_element(languages)
    title = get_title(language)
    page_count = fake.random_int(min=100, max=500)
    inventory_count = fake.random_int(min=10, max=100)
    price = round(fake.pyfloat(left_digits=2, min_value=9, max_value=30), 2)
    print(type(project_number), project_number)

    cursor.execute('''
        INSERT INTO "BOOK" (
            "ISBN",
            "Title",
            "Author",
            "Language",
            "Page_count",
            "Inventory_count",
            "Price",
            "Project_Id"
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (isbn, title, author, language, page_count, inventory_count, price, project_number[0]))

# Commit changes and close connection
conn.commit()
conn.close()
