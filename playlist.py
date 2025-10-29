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
            curs.execute("""
                SELECT 
                    p.pname AS collection_name,
                    COUNT(pcm.movie_id) AS movie_count,
                    COALESCE(
                        FLOOR(SUM(m.length) / 60) ::text || ':' ||
                        LPAD((SUM(m.length) % 60)::text, 2, '0'),
                        '0:00'
                    ) AS total_length
                FROM playlist p
                JOIN user_creates_playlist ucp ON p.playlistid = ucp.playlistid
                LEFT JOIN playlist_contains_movie pcm ON p.playlistid = pcm.playlist_id
                LEFT JOIN movie m ON pcm.movie_id = m.movie_id
                WHERE ucp.username = %s
                GROUP BY p.pname
                ORDER BY p.pname ASC;
            """, (username,))

            rows = curs.fetchall()

            if not rows:
                print("You don’t have any playlists yet.")
                return

            print(f"\nPlaylists for user '{username}':")
            for name, count, total in rows:
                print(f" {name:<25} | Movies: {count:<3} | Total: {total}")

    except Exception as e:
        print("Couldnt get playlists:", e)

    finally:
        conn.close()
        server.stop()