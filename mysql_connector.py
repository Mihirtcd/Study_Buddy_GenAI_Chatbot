# # mysql_connector.py
# import mysql.connector
# from mysql.connector import Error

# def create_db_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             passwd="9717558791Mi#",
#             database="Nudge_Based_MotivationalAgent"
#         )
#         print("MySQL Database connection successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#     return connection

# # Function to execute a read query
# def execute_read_query(connection, query):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")

# # Function to close the connection
# def close_db_connection(connection):
#     if connection.is_connected():
#         connection.close()
#         print("MySQL connection is closed")

# mysql_connector.py
# import mysql.connector
# from mysql.connector import Error

# # Function to create a database connection
# def create_db_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             passwd='9717558791Mi#',
#             database='Nudge_Based_MotivationalAgent'
#         )
#         print("MySQL Database connection successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#     return connection

# # Function to execute a read query
# def execute_read_query(connection, query):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute(query)
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")

# # Function to close the connection
# def close_db_connection(connection):
#     if connection.is_connected():
#         connection.close()
#         print("MySQL connection is closed")

# # The main block to test the database connection and perform a sample query
# if __name__ == "__main__":
#     # Use your actual details here
#     host = "localhost"
#     user = "root"
#     password = "9717558791Mi#"  # Make sure to use the new password you've set
#     database = "Nudge_Based_MotivationalAgent"
    
#     # Create a database connection
#     connection = create_db_connection(host, user, password, database)

#     # If the connection was successful, perform a sample query
#     if connection is not None and connection.is_connected():
#         sample_query = "SELECT * FROM Nudges LIMIT 1;"  # Replace with your actual table name
#         results = execute_read_query(connection, sample_query)

#         # Print the results of the sample query
#         if results:
#             for result in results:
#                 print(result)
#         else:
#             print("No results returned from the database.")

#         # Close the connection
#         close_db_connection(connection)
#     else:
#         print("Failed to connect to the database")

# mysql_connect.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

def execute_query(connection, query, args=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        connection.commit()
        print("Query successful")
    except Error as e:
        print(f"Error: '{e}'")

def execute_read_query(connection, query, args=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, args)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: '{e}'")
