import sqlite3


def add_data(table, data):
    # Adds data to table
    # table: name of table to add data to
    # data: list of values to add to table

    # Connect to database
    conn = sqlite3.connect("pub.db")
    
    if all(value != "" for value in data.values()):
        # Build the SQL query for insertion
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        print(sql_query)

        conn.execute(sql_query)
        conn.commit()
        conn.close()
    else:
        print("Error: All columns must have non-empty values for insertion.")
        conn.close()

def search(table, data):
    # Searches for data in table
    # table: name of table to search in
    # data: dictionary of values to search for
    # returns: list of tuples containing results

    # Connect to database
    conn = sqlite3.connect("pub.db")
    c = conn.cursor()

    # Build the SQL query based on the search criteria
    sql_query = f"SELECT * FROM {table} WHERE 1=1"

    for column, value in data.items():

        if value != "":
            sql_query += f" AND {column} {value}"

    print(sql_query)

    # create lists for displaying results
    columns = [col for col in data.keys()]
    column_mask = [col for col in data.keys() if data[col] != ""]

    # Execute the query and print the results
    results = c.execute(sql_query).fetchall()
    conn.close()
                
    return columns, results, column_mask

def delete(table, data):
    # Deletes data from table
    # table: name of table to delete data from
    # data: dictionary of values to delete

    # Connect to database
    conn = sqlite3.connect("pub.db")
    c = conn.cursor()

    # Build the SQL query based on the search criteria
    sql_query = f"DELETE FROM {table} WHERE 1=1"

    for column, value in data.items():

        if value != "":
            sql_query += f" AND {column} = '{value}'"
    
    print(sql_query)

    # Execute the query and print the results
    c.execute(sql_query)
    conn.commit()
    conn.close()

def update(table, data, where):
    # Updates data in table
    # table: name of table to update data in
    # data: dictionary of values to update
    # where: list to search

    # Connect to database
    conn = sqlite3.connect("pub.db")
    c = conn.cursor()

    # Build the SQL query based on the where criteria
    set_clause = ', '.join([f"{column} = '{value}'" for column, value in data.items()])
    sql_query = f"UPDATE {table} SET {set_clause} WHERE {where[0]} = '{where[1]}'"

    print(sql_query)

    # Execute the query and print the results
    c.execute(sql_query)
    conn.commit()
    conn.close()