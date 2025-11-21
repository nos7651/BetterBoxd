from db import get_connection


def view_trends(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            #find top 20 most popular movies in last 90 days
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
        #top 20 most popular movies among the users the current uesr follows
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

        #top 5 new releases of the current year
        cur.execute("""
            SELECT movie_id, title, release_year
            FROM movie
            WHERE release_year = EXTRACT(YEAR FROM NOW())
            ORDER BY release_year DESC, title ASC
            LIMIT 5;
        """)    
        top_five_this_month = cur.fetchall()
        persist = True
        while(persist):
            print("\n ===== TREND OPTIONS =====")
            print("1. View 20 most popular movies in the last 90 days")
            print("2. View top 20 most popular movies among your following")
            print("3. Find the top 5 new releases of the year!")
            print("4. Exit")

            response = input("Choose an option!: ").strip()
            if response == "1":
                print("\n--- TOP 20: Last 90 Days ---")
                for movie_id, title, count in top_twenty_last_ninety:
                    print(f"{movie_id}: {title} - {count} plays")
                

            elif response == "2":
                print("\n--- TOP 20: Your Following Watched")
                
                if not top_twenty_of_following:
                    print("Users you follow have not watched anything recently!")
                else:
                    for movie_id, title, count in top_twenty_of_following:
                        print(f"{movie_id}: {title} - {count} plays")


            elif response == "3":
                print("\n--- TOP 5 New Releases this Year! ---")
                if not top_five_this_month:
                    print("No new releases found for this year.")
                else:
                    for movie_id, title, year in top_five_this_month:
                        print(f"{movie_id}: {title} ({year})")

            elif response == "4":
                persist = False

            else:
                print("\nInvalid response!  Please say either 1, 2, or 3.")
    
    except Exception as e:
        print("Error fetching trend data.")
    finally:
        conn.close()
        server.stop()