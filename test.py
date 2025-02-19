import psycopg2

# Establish connection
connection = psycopg2.connect(user="postgres", password="scarpion.6159", host="127.0.0.1", port="5432")

# Create a cursor object
cursor = connection.cursor()

# Execute SQL query to list all databases
cursor.execute("SELECT datname FROM pg_database;")

# Fetch all rows
databases = cursor.fetchall()

# Print all database names
print("Databases in PostgreSQL:")
for db in databases:
    print(db[0])  # Each db is a tuple, so db[0] gets the database name

# Close the cursor and connection
cursor.close()
connection.close()
