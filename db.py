import psycopg
from sshtunnel import SSHTunnelForwarder

def get_connection():
    try:
        username = "don5082"
        password = "C3nt3rfi3ldb8sball3r"
        dbname = "p320_41"

        print("Starting tunnel...")
        server = SSHTunnelForwarder(
            ('starbug.cs.rit.edu', 22),
            ssh_username=username,
            ssh_password=password,
            remote_bind_address=('127.0.0.1', 5432)
        )
        server.start()
        print("SSH tunnel established!")

        print(f"Connecting to database {dbname} on port {server.local_bind_port}...")
        conn = psycopg.connect(
            dbname=dbname,
            user=username,
            password=password,
            host='localhost',
            port=server.local_bind_port
        )
        print("Database connection successful.")
        return conn, server
    except Exception as e:
        print("Error connecting to database:", e)

    except KeyboardInterrupt:
        print("User interrupted.")
        conn.close()
        server.stop()

if __name__ == "__main__":
    conn, server = get_connection()
    print("Connection successful!")
    conn.close()
    server.stop()
