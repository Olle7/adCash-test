import sqlite3

# Connect to the database (create a new database if it doesn't exist)
conn = sqlite3.connect('loan_applications.db')

# Create a new table for loan applications

## amount,currency,term,name,ID,contact,type_of_contact,comment
conn.execute('''
CREATE TABLE IF NOT EXISTS loan_database (
    amount FLOAT,
    currency TEXT,
    term FLOAT,
    name TEXT,
    personal_id INTEGER,
    contact TEXT,
    type_of_contact TEXT,
    comment TEXT,
    time_of_recieving_application INTEGER
);
''')
conn.execute("""
CREATE TABLE IF NOT EXISTS blacklisted_personal_IDs (
    id INTEGER PRIMARY KEY,
    personal_id INTEGER
);""")


# Commit the changes and close the connection
conn.commit()
conn.close()
