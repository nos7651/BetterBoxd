from db import get_connection

def create_playlist(username, playlist_name):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                INSERT INTO playlist(playlist_name)
                VALUES(%s)
                RETURNING playlist_id;
                """, (playlist_name,))
            playlist_id = curs.fetchone()[0]

            curs.execute("""
                INSERT INTO user_creates_playlist(playlist_id, username)
                VALUES(%s, %s);
                """, (playlist_id, username))

            conn.commit()
            print(f"Playlist '{playlist_name}' created for user '{username}' (ID: {playlist_id}).")
    except Exception as e:
        print("Playlist wasnt created",e)
    finally:
        conn.close()
        server.stop()


def view_playlists(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute(r"""
                SELECT 
                    p.playlist_id,
                    p.playlist_name AS collection_name,
                    COUNT(pcm.movie_id) AS movie_count,
                    COALESCE(
                        FLOOR(SUM(COALESCE(m.length, 0)) / 60)::text || ':' ||
                        LPAD((SUM(COALESCE(m.length, 0)) %% 60)::text, 2, '0'),
                        '0:00'
                    ) AS total_length
                FROM playlist p
                JOIN user_creates_playlist ucp ON p.playlist_id = ucp.playlist_id
                LEFT JOIN playlist_contains_movie pcm ON p.playlist_id = pcm.playlist_id
                LEFT JOIN movie m ON pcm.movie_id = m.movie_id
                WHERE ucp.username = %s
                GROUP BY p.playlist_id, p.playlist_name
                ORDER BY p.playlist_name ASC;
            """, (username,))

            rows = curs.fetchall()

            if not rows:
                print("You don’t have any playlists yet.")
                return

            print(f"\nPlaylists for user '{username}':")
            for pid, name, count, total in rows:
                print(f" ID: {pid:<4} | {name:<25} | Movies: {count:<3} | Total: {total}")

    except Exception as e:
        print("Couldnt get playlists:", e)

    finally:
        conn.close()
        server.stop()

def add_movie_to_playlist(username, playlist_id, movie_id):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT 1 FROM playlist_contains_movie 
                WHERE movie_id = %s AND playlist_id = %s;
            """, (movie_id, playlist_id))
            exists = curs.fetchone()
            if exists:
                print(f"Movie {movie_id} is already in playlist {playlist_id}.")
                return

            curs.execute("""
                SELECT COUNT(*) 
                FROM user_watches_movie
                WHERE username = %s AND movie_id = %s;
            """, (username, movie_id))
            result = curs.fetchone()
            times_watched = result[0] if result else 0

            curs.execute("""
            INSERT INTO playlist_contains_movie(playlist_id, movie_id, times_watched)
            VALUES (%s, %s, %s);
            """, (playlist_id, movie_id, times_watched))

            conn.commit()
            print(f"Movie {movie_id} added to playlist {playlist_id}.")

    except Exception as e:
        print("Couldnt add movie:", e)

    finally:
        conn.close()
        server.stop()

def remove_movie_from_playlist(playlist_id, movie_id):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT 1 FROM playlist_contains_movie
                WHERE playlist_id = %s AND movie_id = %s;
            """, (playlist_id, movie_id))
            exists = curs.fetchone()

            if not exists:
                print(f"Movie {movie_id} is not in playlist {playlist_id}.")
                return

            curs.execute("""
                DELETE FROM playlist_contains_movie
                WHERE playlist_id = %s AND movie_id = %s;
            """, (playlist_id, movie_id))

            conn.commit()
            print(f"Movie {movie_id} successfully removed from playlist {playlist_id}.")

    except Exception as e:
        print("Error removing movie from playlist:", e)

    finally:
        conn.close()
        server.stop()

def rename_playlist(playlist_id, new_name):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT playlist_id, playlist_name
                FROM playlist
                WHERE playlist_id = %s;
            """, (playlist_id,))
            existing = curs.fetchone()

            if not existing:
                print(f"Playlist with ID {playlist_id} does not exist.")
                return

            curs.execute("""
                UPDATE playlist
                SET playlist_name = %s
                WHERE playlist_id = %s;
            """, (new_name, playlist_id))

            conn.commit()
            print(f"Playlist renamed to '{new_name}' (ID: {playlist_id}).")

    except Exception as e:
        print("Error renaming playlist:", e)

    finally:
        conn.close()
        server.stop()

def watch_playlist(playlist_id):
    conn, server = get_connection()

    try:

        with conn.cursor() as curs:
            curs.execute("""
                UPDATE playlist_contains_movie
                SET times_watched = times_watched + 1
                WHERE playlist_id = %s;
            """, (playlist_id,))

        print("Playlist watched.")

    except Exception as e:
        print("Error renaming playlist:", e)

    finally:
        conn.close()
        server.stop()

def delete_playlist(playlist_id, username):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            curs.execute("""
                SELECT 1 FROM user_creates_playlist
                WHERE user_creates_playlist.playlist_id = %s AND username = %s;
            """, (playlist_id, username))
            owned = curs.fetchone()

            if not owned:
                print(f"Playlist {playlist_id} does not belong to user '{username}'.")
                return

            curs.execute("""
                DELETE FROM playlist_contains_movie
                WHERE playlist_id = %s;
            """, (playlist_id,))

            curs.execute("""
                DELETE FROM user_creates_playlist
                WHERE user_creates_playlist.playlist_id = %s;
            """, (playlist_id,))

            curs.execute("""
                DELETE FROM playlist
                WHERE playlist_id = %s;
            """, (playlist_id,))

            conn.commit()
            print(f"Playlist {playlist_id} deleted successfully.")

    except Exception as e:
        print("Couldnt create playlist:", e)

    finally:
        conn.close()
        server.stop()