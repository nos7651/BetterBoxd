from db import get_connection

def create_user(username, password, email, first_name, last_name ):
    if len(username) > 50 or len(first_name) > 50 or len(last_name) > 50:
        print("Error: Username cannot be longer than 50 characters.")
        return
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
        print("connection closed")


def login(username, password):

    conn, server = get_connection()
    try:
        with conn.cursor() as cur:

            cur.execute("SELECT password FROM app_user WHERE username = %s", (username,))
            result = cur.fetchone()

            if not result:
                print("No such user found.")
                return False

            stored_password = result[0]


            if stored_password != password:
                print("Incorrect password.")
                return False


            cur.execute("""
                UPDATE app_user
                SET last_access_ts = NOW()
                WHERE username = %s;
            """, (username,))
            conn.commit()

            print(f"Login successful! Welcome back, {username}.")
            return True

    except Exception as e:
        conn.rollback()
        print("Error during login:", e)
        conn.close()
        server.stop()
        return False
    finally:
        conn.close()
        server.stop()
        print("connection closed")

def rate_movie(username, movie_id, star_rating):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_rates_movie (username, movie_id, star_rating)
                    VALUES (%s, %s, %s)
            """, (username, movie_id, str(star_rating)))
            conn.commit()
    except Exception as e:
        print("Error during rating:", e)

    except KeyboardInterrupt:
        print("User interrupted.")
        
    finally:
        conn.close()
        server.stop()
