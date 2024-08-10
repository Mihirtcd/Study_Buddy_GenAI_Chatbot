# The main block to test the database connection and perform a sample query
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