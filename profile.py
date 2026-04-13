# Import the database connection function
from db import get_connection

# Function to fetch and display a user's profile with ratings
def get_user_profile_rating(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Fetch the number of playlists created by the user
            cur.execute("""
                   SELECT COUNT(*)
                   FROM user_creates_playlist
                   WHERE username = %s;   
                   """, (username,))
            playlist_count = cur.fetchone()[0]

            # Fetch the number of followers the user has
            cur.execute("""
                   SELECT COUNT(*)
                       FROM user_follows_user
                       WHERE followed_username = %s;
                   """, (username,))
            follower_count = cur.fetchone()[0]

            # Additional queries to fetch user profile data
            # number of people you're following
            cur.execute("""
               SELECT COUNT(*)
                   FROM user_follows_user
                   WHERE follower_username = %s;
                   """, (username,))
            following_count = cur.fetchone()[0]

            # top 10 movies by rating
            cur.execute("""
               SELECT m.title, ur.star_rating
               FROM user_rates_movie ur
               JOIN movie m ON m.movie_id = ur.movie_id
               WHERE ur.username = %s
               ORDER BY ur.star_rating DESC
               LIMIT 10;
           """, (username,))
            top_movies = cur.fetchall()

        # Print the user's profile details
        print("\n===== USER PROFILE =====")
        print(f"User: {username}")
        print(f"Playlists created: {playlist_count}")
        print(f"Followers: {follower_count}")
        print(f"Following: {following_count}")

        print("\nTop 10 Movies:")
        if not top_movies:
            # Handle case where no top movies are found
            print("  No rated movies yet.")
        else:
            for title, rating in top_movies:
                print(f"  {title}  — {rating} stars")

    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error fetching profile:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to fetch and display a user's watched movies
def get_user_profile_watched(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Logic to fetch watched movies goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error fetching profile:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to fetch and display a user's mixed profile
def get_user_profile_mix(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # number of playlists
            cur.execute("""
                   SELECT COUNT(*)
                   FROM user_creates_playlist
                   WHERE username = %s;


                       """, (username,))
            playlist_count = cur.fetchone()[0]
            # number of followers
            cur.execute("""
                   SELECT COUNT(*)
                       FROM user_follows_user
                       WHERE followed_username = %s;


                       """, (username,))
            follower_count = cur.fetchone()[0]
            # number of people you're following
            cur.execute("""
               SELECT COUNT(*)
                   FROM user_follows_user
                   WHERE follower_username = %s;
                   """, (username,))
            following_count = cur.fetchone()[0]
            # top 10 movies by combination of rating and plays
            cur.execute("""
               WITH movie_stats AS (
                   SELECT
                       m.movie_id,
                       m.title,
                       COALESCE(ur.star_rating, 0) AS rating,
                       COUNT(uwm.movie_id) AS play_count
                   FROM movie m
                   LEFT JOIN user_rates_movie ur
                       ON ur.movie_id = m.movie_id AND ur.username = %s
                   LEFT JOIN user_watches_movie uwm
                       ON uwm.movie_id = m.movie_id AND uwm.username = %s
                   WHERE ur.username = %s OR uwm.username = %s
                   GROUP BY m.movie_id, m.title, ur.star_rating
               )
               SELECT
                   title,
                   rating,
                   play_count,
                   (rating * 0.6 + play_count * 0.4) AS combined_score
               FROM movie_stats
               WHERE rating > 0 OR play_count > 0
               ORDER BY combined_score DESC, title ASC
               LIMIT 10;
           """, (username, username, username, username))
            top_movies = cur.fetchall()

        # Print the user's profile details
        print("\n===== USER PROFILE =====")
        print(f"User: {username}")
        print(f"Playlists created: {playlist_count}")
        print(f"Followers: {follower_count}")
        print(f"Following: {following_count}")

        print("\nTop 10 Movies (by Rating + Plays Combined):")
        if not top_movies:
            # Handle case where no top movies are found
            print("  No movies rated or watched yet.")
        else:
            for title, rating, play_count, score in top_movies:
                rating_str = f"{rating} stars" if rating > 0 else "Not rated"
                print(f"  {title}  — {rating_str}, {play_count} plays")

    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error fetching profile:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()


