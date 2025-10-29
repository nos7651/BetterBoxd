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