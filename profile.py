from db import get_connection

def get_user_profile(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            #number of playlists 
            cur.execute("""
                    SELECT COUNT(*)
                    FROM user_creates_playlist
                    WHERE username = %s;    

                        """, (username,))     
            playlist_count = cur.fetchone()[0]
            #number of followers
            cur.execute("""
                    SELECT COUNT(*)
                        FROM user_follows_user
                        WHERE followed_username = %s;

                        """, (username))   
            follower_count = cur.fetchone()[0]   
            #number of people you're following
            cur.execute("""
                SELECT COUNT(*)
                    FROM user_follows_user
                    WHERE follower_username = %s;
                    """, (username))      
            following_count = cur.fetchone()[0]
            #top 10 movies by rating
            cur.execute("""
                SELECT m.title, ur.star_rating
                FROM user_rates_movie ur
                JOIN movie m ON m.movie_id = ur.movie_id
                WHERE ur.username = %s
                ORDER BY ur.star_rating DESC
                LIMIT 10;
            """, (username,))
            top_movies = cur.fetchall()
        
        #printing results
        print("\n===== USER PROFILE =====")
        print(f"User: {username}")
        print(f"Playlists created: {playlist_count}")
        print(f"Followers: {follower_count}")
        print(f"Following: {following_count}")

        print("\nTop 10 Movies:")
        if not top_movies:
            print("  No rated movies yet.")
        else:
            for title, rating in top_movies:
                print(f"  {title}  — {rating} stars")

    except Exception as e:
        print("Error fetching profile:", e)
    finally:
        conn.close()
        server.stop()


