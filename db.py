import psycopg2
from sshtunnel import SSHTunnelForwarder



def get_connection():
    username = "don5082"
    password = "C3nt3rfi3ldb8sball3r"
    db_name = "p320_41"
    server = SSHTunnelForwarder(
        ('starbug.cs.rit.edu', 22),
        ssh_username=username,
        ssh_password=password,
        remote_bind_address=('127.0.0.1', 5432)
    )
    server.start()

    params = {
        'dbname': db_name,
        'user': username,
        'password': password,
        'host': 'localhost',
        'port': server.local_bind_port
    }

    conn = psycopg2.connect(**params)
    return conn, server

if __name__ == "__main__":
    conn, server = get_connection()
    print("Connection successful!")
    conn.close()
    server.stop()

