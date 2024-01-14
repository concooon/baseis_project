import sqlite3


def add_data(table, data):
    # Adds data to table
    # table: name of table to add data to
    # data: list of values to add to table
    # returns: True if successful, False if not

    # Connect to database
    conn = sqlite3.connect("database.db")
    
    if all(value != "" for value in data.values()):
        # Build the SQL query for insertion
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        conn.execute(sql_query)
        conn.commit()
        conn.close()
        return True
    else:
        print("Error: All columns must have non-empty values for insertion.")
        conn.close()
        return False

def search(table, data):
    # Searches for data in table
    # table: name of table to search in
    # data: dictionary of values to search for
    # returns: list of tuples containing results

    # Connect to database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Build the SQL query based on the search criteria
    sql_query = f"SELECT * FROM {table} WHERE 1=1"

    for column, value_info in data.items():
        value, use_exact_match = value_info

        if value != "":
            if use_exact_match:
                sql_query += f" AND {column} = '{value}'"
            else:
                sql_query += f" AND {column} LIKE '%{value}%'"

    # create lists for displaying results
    columns = [col for col in data.keys()]
    column_mask = [col for col in data.keys() if data[col][0] != ""]

    # Execute the query and print the results
    results = c.execute(sql_query).fetchall()
    conn.close()
                
    return columns, results, column_mask