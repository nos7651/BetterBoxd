# Import the database connection function
from db import get_connection

# Function to view trending movies based on different criteria
def view_trends(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            # Query to find the top 20 most popular movies in the last 90 days
            cur.execute("""
            SELECT
                m.movie_id,
                m.title,
                COUNT(uwm.movie_id) AS watch_count
            FROM user_watches_movie uwm
            JOIN movie m ON m.movie_id = uwm.movie_id
            WHERE uwm.date >= NOW() - INTERVAL '90 days'
            GROUP BY m.movie_id
            ORDER BY watch_count DESC
            LIMIT 20;
            """)
            top_twenty_last_ninety = cur.fetchall()

            # Query to find the top 20 most popular movies among the users the current user follows
            cur.execute("""
                SELECT
                    m.movie_id,
                    m.title,
                    COUNT(uwm.movie_id) AS watch_count
                FROM user_follows_user ufu
                JOIN user_watches_movie uwm
                    ON ufu.followed_username = uwm.username
                JOIN movie m
                    ON m.movie_id = uwm.movie_id
                WHERE ufu.follower_username = %s
                AND uwm.date >= NOW() - INTERVAL '90 days'
                GROUP BY m.movie_id
                ORDER BY watch_count DESC
                LIMIT 20;
                """, (username,))
            top_twenty_of_following = cur.fetchall()

            # Query to find the top 5 new releases of the current year
            cur.execute("""
                SELECT
                m.movie_id,
                m.title,
                COUNT(uwm.movie_id) AS watch_count
            FROM user_watches_movie uwm
            JOIN movie m ON m.movie_id = uwm.movie_id
            WHERE uwm.date >= DATE_TRUNC('year', CURRENT_DATE)
            GROUP BY m.movie_id
            ORDER BY watch_count DESC
            LIMIT 5;
            """)    
            top_five_this_month = cur.fetchall()

            # Display trend options to the user
            persist = True
            while(persist):
                print("\n ===== TREND OPTIONS =====")
                print("1. View 20 most popular movies in the last 90 days")
                print("2. View top 20 most popular movies among your following")
                print("3. Find the top 5 new releases of the year!")
                print("4. Exit")

                response = input("Choose an option!: ").strip()

                # Logic to handle user input goes here
                pass
    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Error fetching trend data.")
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()