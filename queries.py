from db import get_connection

def create_user(username, password, email, first_name, last_name ):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO app_user (username, password, email, first_name, last_name, creation_date, last_access_ts)
                        VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
                        """, (username, password, email, first_name, last_name))
            conn.commit()
            print("User created successfully!")
    except Exception as e:
        print("Error creating user:", e)
    finally:
        conn.close()
        server.stop()