import psycopg2
from sshtunnel import SSHTunnelForwarder

username = "don5082"
password = "C3nt3rfi3ldb8sball3r"
dbName = "p320_41"


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        print("SSH tunnel established")
        params = {
            'dbname': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        #DB work here....

        conn.close()
except Exception as e:
    print("Connection failed:", e)
