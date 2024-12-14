import mysql.connector
from mysql.connector import Error

# Function to establish a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="parkingdata"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error: ", e)
        return None

# Function to execute SQL queries
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print("Error: ", e)

# Function to show all data from the table
def show_all_data(connection):
    select_all_query = "SELECT * FROM parkinginfo"
    cursor = connection.cursor()
    cursor.execute(select_all_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Function to calculate time stayed
def calculate_time_stayed(arrival_time, departure_time):
    arrival = datetime.strptime(arrival_time, '%H:%M:%S')
    departure = datetime.strptime(departure_time, '%H:%M:%S')
    if departure>arrival:
        time_stayed = departure - arrival
    else :
        time_stayed=departure+'24:00:00'-arrival
    return time_stayed.total_seconds() / 3600  # Convert seconds to hours

# Function to insert data
def insert_data(connection, owner, arrival_time, departure_time, plate_number):
    if None in (owner, arrival_time, departure_time, plate_number):
        print("Error: All values must be provided (except time of departure)")
        return

    insert_query = f"""
    INSERT INTO parkinginfo (Owner, TimeOfArrival, TimeOfDeparture, PlateNumber)
    VALUES ('{owner}', '{arrival_time}', '{departure_time}', '{plate_number}')
    """
    execute_query(connection, insert_query)

# Function to calculate cost
def calculate_cost(time_stayed):
    initial_cost = 20
    hourly_rate = 20 + ((time_stayed // 2) * 5)
    total_cost = max(initial_cost, hourly_rate)
    return total_cost
# Function for driver alarm
def driver_alarm():
    print("Driver alarm! It's been 3 hours. Please check and move your vehicle.")

# Main function
def main():
    # Create a connection
    connection = create_connection()

    if connection:
        # Uncomment the following lines if you want to create the database and table
        # execute_query(connection, "CREATE DATABASE IF NOT EXISTS parkingdata")
        # execute_query(connection, "USE parkingdata")
        # execute_query(connection, """
        #     CREATE TABLE IF NOT EXISTS parkinginfo (
        #         Owner VARCHAR(255),
        #         TimeOfArrival TIME,
        #         TimeOfDeparture TIME,
        #         PlateNumber VARCHAR(20)
        #     )
        # """)

        # Show all data from the table
        print("All data from the table:")
        show_all_data(connection)

        # Example: Calculate time stayed
        arrival_time = "09:15:00"
        departure_time = "12:30:00"
        time_stayed = calculate_time_stayed(arrival_time, departure_time)
        print(f"Time Stayed: {time_stayed:.2f} hours")

        # Example: Insert data
        insert_data(connection, "NewOwner", "12:00:00", "15:30:00", "NEW-001")

        # Show updated data from the table
        print("\nAll data from the table after insertion:")
        show_all_data(connection)

        # Example: Calculate cost
        cost = calculate_cost(time_stayed)
        print(f"Cost for time stayed: {cost:.2f} rupees")

        # Example: Driver alarm
        driver_alarm()

        # Close the connection
        connection.close()

# Create a connection
connection = create_connection()

if connection:
    # SQL query to create the database
    create_database_query = "CREATE DATABASE IF NOT EXISTS parkingdata"

    # SQL query to use the parkingdata database
    use_database_query = "USE parkingdata"

    # SQL query to create the parkinginfo table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS parkinginfo (
        Owner VARCHAR(255),
        TimeOfArrival TIME,
        TimeOfDeparture TIME,
        PlateNumber VARCHAR(20)
    )
    """

    # SQL queries to insert data into the parkinginfo table
    insert_data_queries = """
    INSERT INTO parkinginfo (Owner, TimeOfArrival, TimeOfDeparture, PlateNumber)
    VALUES
        ('Smith', '09:15:00', '12:30:00', 'ABC-123'),
        ('Johnson', '10:30:00', '14:45:00', 'XYZ-789'),
        ('Williams', '11:45:00', '15:15:00', 'DEF-456'),
        ('Davis', '13:00:00', '16:45:00', 'GHI-789'),
        ('Taylor', '14:15:00', '18:00:00', 'JKL-012'),
        ('Anderson', '15:30:00', '19:30:00', 'MNO-345'),
        ('Martinez', '16:45:00', '20:15:00', 'PQR-678'),
        ('Jackson', '18:00:00', '21:45:00', 'STU-901'),
        ('White', '19:15:00', '23:00:00', 'VWX-234'),
        ('Harris', '20:30:00', '00:30:00', 'YZA-567'),
        ('Clark', '21:45:00', '01:15:00', 'BCD-890'),
        ('Lewis', '23:00:00', '02:45:00', 'EFG-123'),
        ('Lee', '00:15:00', '04:15:00', 'HIJ-456'),
        ('Walker', '01:30:00', '05:45:00', 'KLM-789'),
        ('Hall', '02:45:00', '07:15:00', 'NOP-012'),
        ('Allen', '04:00:00', '08:45:00', 'QRS-345'),
        ('Turner', '05:15:00', '10:15:00', 'TUV-678'),
        ('Baker', '06:30:00', '11:45:00', 'WXY-901'),
        ('Gonzalez', '07:45:00', '13:30:00', 'ZAB-234'),
        ('Thomas', '09:00:00', '15:00:00', 'CDE-567')
    """

    # Execute the queries
    execute_query(connection, create_database_query)
    execute_query(connection, use_database_query)
    execute_query(connection, create_table_query)
    execute_query(connection, insert_data_queries)

    # Close the connection
    connection.close()
