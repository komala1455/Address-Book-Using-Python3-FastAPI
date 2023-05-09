import sqlite3

# Create a connection to the database
conn = sqlite3.connect('address.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define a SQL statement to create a table
create_table = '''CREATE TABLE IF NOT EXISTS address
    (id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code INTEGER NOT NULL,
    latitude TEXT NOT NULL,
    longitude TEXT NOT NULL)'''

# Execute the SQL statement
cursor.execute(create_table)

# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()
