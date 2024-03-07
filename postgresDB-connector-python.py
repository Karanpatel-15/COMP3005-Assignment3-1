import psycopg2
from configparser import ConfigParser


def load_config(filename='database.ini', section='postgresql'):
    """ Load the configuration file and return a dictionary object (database connection parameters)
    """
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def connect(config):
    """ Connect to the PostgreSQL database server and return a connection object
    """
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
 
def tables(conn):
    """ List all tables in the database
    """
    try:
        with conn.cursor() as cur:  # Create a new cursor (used to execute SQL commands)
            cur.execute("/dt") 
            rows = cur.fetchall()   # Fetch all the rows from the last executed statement
            for row in rows:        # Print each row
                print(row)
    except (psycopg2.DatabaseError, Exception) as error: # Catch any exceptions and print the error
        print(error)

def selectAll(conn, table_name):
    """ Select all rows from the table
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM " + table_name)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def insert(conn, table_name, columns, values):
    """ Insert a new row into the table
    """
    try:
        with conn.cursor() as cur:  
            cur.execute("INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")") 
            conn.commit()           # Commit the changes to the database
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def update(conn, table_name, column, value, condition):
    """ Update a row in the table
    """
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE " + table_name + " SET " + column + " = " + value + " WHERE " + condition)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete(conn, table_name, condition):
    """ Delete a row from the table
    """
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM " + table_name + " WHERE " + condition)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def consoleStudentApplication(conn):
    """ Console application for the student database
    """

    print("Welcome to the Student Database Application")
    while True:
        try:
            print("\n1. View all students")
            print("2. Add a new student")
            print("3. Update a student's email")
            print("4. Delete a student")
            print("5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                selectAll(conn, 'students')
            elif choice == 2:
                first_name = input("Enter the student's first name: ")
                last_name = input("Enter the student's last name: ")
                email = input("Enter the student's email: ")
                enrollment_date = input("Enter the student's enrollment date (format: 2023-09-02): ")
                insert(conn, 'students', 'first_name, last_name, email, enrollment_date', "'" + first_name + "', '" + last_name + "', '" + email + "', '" + enrollment_date + "'")
            elif choice == 3:
                student_id = input("Enter the student's ID: ")
                new_email = input("Enter the student's new email: ")
                update(conn, 'students', 'email', "'" + new_email + "'", 'student_id = ' + student_id)
            elif choice == 4:
                student_id = input("Enter the student's ID: ")
                delete(conn, 'students', 'student_id = ' + student_id)
            elif choice == 5:
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid choice. Try again.")
    print("Goodbye!")

if __name__ == '__main__':
    # Load the configuration file get the connection parameters like host, database, user, password, etc.
    config = load_config() 
    # Connect to the PostgreSQL database server
    conn = connect(config)
    # Run the console application
    consoleStudentApplication(conn);




