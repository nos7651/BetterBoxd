# Import the database connection function
from db import get_connection

# Function to search for a user by email
def search_user(email: str):
    conn, server = get_connection()
    try:
        # Query the database for a user with the given email
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT username, email
                FROM app_user AS u
                WHERE LOWER(u.email) = LOWER(%s)
                """,
                (email,)
            )
            row = cur.fetchone()

            if not row:
                # Handle case where no user is found
                pass

            username = row[0]
            print("Results:")
            print(username)
            return username

    except Exception as e:
        # Handle any exceptions that occur during the query
        print("Error fetching users:", e)
        return None
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to follow another user
def follow_user(current_user, target_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Ensure the target user exists
            cur.execute("SELECT username FROM app_user WHERE username = %s;", (target_user,))
            result = cur.fetchone()
            if not result:
                # Handle case where target user does not exist
                pass
            if current_user == target_user:
                # Prevent users from following themselves
                pass
            # Insert a follow relationship into the database
            cur.execute("""
                INSERT INTO user_follows_user (followed_username, follower_username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (target_user, current_user))
            conn.commit()

    except Exception as e:
        # Handle any exceptions that occur during the follow operation
        print("Error following user:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to unfollow a user
def unfollow_user(current_user, target_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Logic to remove a follow relationship goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the unfollow operation
        print("Error unfollowing user:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to list users that the current user is following
def list_following(current_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Logic to fetch the list of followed users goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error listing following list:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()
        print("connection closed")

# Function to list followers of the current user
def list_followers(current_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Logic to fetch the list of followers goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error fetching followers:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to check if the current user is following another user
def is_following(current_user, target_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Logic to check the follow status goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the check operation
        print("Error checking following status:", e)
        return False
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()
