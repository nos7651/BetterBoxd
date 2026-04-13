# Import the database connection function
from db import get_connection

# Function to create a new playlist for a user
def create_playlist(username, playlist_name):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            # Insert the playlist into the database and get its ID
            curs.execute("""
                INSERT INTO playlist(playlist_name)
                VALUES(%s)
                RETURNING playlist_id;
                """, (playlist_name,))
            playlist_id = curs.fetchone()[0]

            # Associate the playlist with the user
            curs.execute("""
                INSERT INTO user_creates_playlist(playlist_id, username)
                VALUES(%s, %s);
                """, (playlist_id, username))

            conn.commit()
            print(f"Playlist '{playlist_name}' created for user '{username}' (ID: {playlist_id}).")
    except Exception as e:
        # Handle any exceptions that occur during playlist creation
        print("Playlist wasnt created", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to view all playlists of a user
def view_playlists(username):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            # Logic to fetch playlists goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the fetch operation
        print("Couldnt get playlists:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Function to add a movie to a playlist
def add_movie_to_playlist(username, playlist_id, movie_id):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            # Logic to add a movie to the playlist goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the add operation
        print("Couldnt add movie:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()

# Additional playlist management functions
# ...existing code...

# Function to delete a playlist
def delete_playlist(playlist_id, username):
    conn, server = get_connection()
    try:
        with conn.cursor() as curs:
            # Logic to delete the playlist goes here
            pass
    except Exception as e:
        # Handle any exceptions that occur during the delete operation
        print("Couldnt create playlist:", e)
    finally:
        # Ensure the connection and server are closed
        conn.close()
        server.stop()