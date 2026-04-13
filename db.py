# Import necessary libraries for database connection and SSH tunneling
import psycopg
from sshtunnel import SSHTunnelForwarder

# Function to establish a connection to the database through an SSH tunnel
def get_connection():
    try:
        # Database and SSH credentials
        username = "xxx"  #This part of the code will be the breaking point as the database isn't connected anymore.
        password = "xxx"
        dbname = "xxx"

        # Establish an SSH tunnel to the remote server
        server = SSHTunnelForwarder(
            ('starbug.cs.rit.edu', 22),
            ssh_username=username,
            ssh_password=password,
            remote_bind_address=('127.0.0.1', 5432)
        )
        server.start()

        # Connect to the database using the SSH tunnel
        conn = psycopg.connect(
            dbname=dbname,
            user=username,
            password=password,
            host='localhost',
            port=server.local_bind_port
        )
        return conn, server
    except Exception as e:
        # Handle any exceptions that occur during the connection process
        print("Error connecting to database:", e)

    except KeyboardInterrupt:
        # Handle user interruption
        conn.close()
        server.stop()

# Main block to test the database connection
if __name__ == "__main__":
    conn, server = get_connection()
    conn.close()
    server.stop()
