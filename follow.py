from db import get_connection
# follow another user

def search_user(email: str):
    conn, server = get_connection()
    try:
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
                print(f"User with email '{email}' does not exist.")
                return None

            username = row[0]
            print("Results:")
            print(username)
            return username

    except Exception as e:
        print("Error fetching users:", e)
        return None
    finally:
        conn.close()
        server.stop()

def follow_user(current_user, target_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            #ensure the target is existent
            cur.execute("SELECT username FROM app_user WHERE username = %s;", (target_user,))
            result = cur.fetchone()
            if not result:
                print(f"User '{target_user}' does not exist.")
                return
            if current_user == target_user:
                print("You cannot follow yourself!")
                return
            cur.execute("""
                INSERT INTO user_follows_user (followed_username, follower_username)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (target_user, current_user))
            conn.commit()
            print(f" You are now following {target_user}.!")

    except Exception as e:
        print("Error following user:", e)
    finally:
        conn.close()
        server.stop()



def unfollow_user(current_user, target_user):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM user_follows_user
                WHERE followed_username = %s AND follower_username = %s;
            """, (target_user, current_user))
            conn.commit()
            print(f"You unfollowed {target_user}.")
    except Exception as e:
        print("Error unfollowing user:", e)
    finally:
        conn.close()
        server.stop()



def list_following(current_user):
    conn, server =  get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT followed_username
                FROM user_follows_user
                WHERE follower_username = %s;
            """, (current_user,))
            follows = [row[0] for row in cur.fetchall()]
            if not follows:
                print(f"{current_user} is not following anyone.")
            else:
                print(f"{current_user} is now following:")
                for user in follows:
                    print(f" - {user}")
    except Exception as e:
        print("Error listing following list:", e)
    finally:
        conn.close()
        server.stop()
        print("connection closed")

def list_followers(current_user):
    conn, server =  get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT follower_username
                FROM user_follows_user
                WHERE followed_username = %s;
            """, (current_user,))
            followers = [row[0] for row in cur.fetchall()]
            if not followers:
                print(f"{current_user} has no followers yet.")
            else:
                print(f"{current_user} is followed by:")
                for user in followers:
                    print(f" - {user}")
    except Exception as e:
        print("Error fetching followers:", e)
    finally:
        conn.close()
        server.stop()

def is_following(current_user, target_user):

    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 1
                FROM user_follows_user
                WHERE follower_username = %s
                  AND followed_username = %s;
            """, (current_user, target_user))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print("Error checking following status:", e)
        return False
    finally:
        conn.close()
        server.stop()
