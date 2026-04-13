# Import the database connection function and bcrypt for password hashing
from db import get_connection
import bcrypt

# Function to create a new user in the database
def create_user(username, password, email, first_name, last_name):
    if len(username) > 50 or len(first_name) > 50 or len(last_name) > 50:
        # Validate input lengths
        print("Error: Username cannot be longer than 50 characters.")
        return
    conn, server = get_connection()

    # Hash the user's password for secure storage
    pass_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    pass_hash_str = pass_hash.decode('utf-8')

    try:
        with conn.cursor() as cur:
            # Insert the new user into the database
            cur.execute("""
                    INSERT INTO app_user (username, password, email, first_name, last_name, creation_date, last_access_ts)
                    VALUES (%s, %s, %s, %s, %s, NOW(), NOW());
                    """, (username, pass_hash_str, email, first_name, last_name))
            conn.commit()
            print("User created successfully!")
    except Exception as e:
        # Handle any exceptions that occur during user creation
        print("Error creating user:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()
        print("connection closed")

# Function to log in a user
def login(username, password):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Fetch the stored password hash for the given username
            cur.execute("SELECT password FROM app_user WHERE username = %s", (username,))
            result = cur.fetchone()

            if not result:
                # Handle case where the user does not exist
                print("No such user found.")
                return False

            stored_pass_hash = result[0].encode('utf-8')

            # Verify the provided password against the stored hash
            if not bcrypt.checkpw(password.encode(), stored_pass_hash):
                print("Incorrect password.")
                return False

            # Update the last access timestamp for the user
            cur.execute("""
                UPDATE app_user
                SET last_access_ts = NOW()
                WHERE username = %s;
            """, (username,))
            conn.commit()

            print(f"Login successful! Welcome back, {username}.")
            return True

    except Exception as e:
        # Handle any exceptions that occur during login
        conn.rollback()
        print("Error during login:", e)
        conn.close()
        server.stop()
        return False
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()
        print("connection closed")

# Function to rate a movie
def rate_movie(username, movie_id, star_rating):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Insert the user's rating for the movie into the database
            cur.execute("""
                INSERT INTO user_rates_movie (username, movie_id, star_rating)
                    VALUES (%s, %s, %s)
            """, (username, movie_id, str(star_rating)))
            conn.commit()
    except Exception as e:
        # Handle any exceptions that occur during the rating process
        print("Error during rating:", e)
    except KeyboardInterrupt:
        # Handle user interruption
        print("User interrupted.")
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()
