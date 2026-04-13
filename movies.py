# Import the database connection function
from db import get_connection

# Globals to store the last search query and parameters
last_where = None
last_params = None

# Function to print movie details from a list of rows
def print_movies(rows):
    if not rows:
        # Handle case where no movies are found
        pass
    print("\nResults:")
    for movie_id, title, length, mpaa, cast_names, director_names, avg_user_rating in rows:
        # Print movie details
        pass
    return 1

# Function to fetch movies based on a query
def get_movies(where_sql: str, params: tuple, order_sql: str = "m.title ASC"):
    conn, server = get_connection()
    try:
        # Logic to execute the query and fetch movies goes here
        pass
    except Exception as e:
        # Handle any exceptions that occur during the query
        pass
    finally:
        # Ensure the connection and server are closed
        pass

# Function to search for movies by title
def search_movie_title(term: str):
    global last_where, last_params
    where = "WHERE LOWER(m.title) LIKE LOWER(%s)"
    params = (f"%{term}%",)
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")

# Function to search for movies by cast member
def search_movie_cast(term: str):
    global last_where, last_params
    where = """
    WHERE EXISTS (
        SELECT 1
        FROM contributor_acts_movie cam
        JOIN contributor c ON c.con_id = cam.con_id
        WHERE cam.movie_id = m.movie_id AND LOWER(c.name) LIKE LOWER(%s)
    )
    OR EXISTS (
        SELECT 1
        FROM contributor_directs_movie cdm
        JOIN contributor c2 ON c2.con_id = cdm.con_id
        WHERE cdm.mov_id = m.movie_id AND LOWER(c2.name) LIKE LOWER(%s)
    )
    """
    params = (f"%{term}%", f"%{term}%")
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")

# Function to search for movies by studio
def search_movie_studio(term: str):
    global last_where, last_params
    where = """
    WHERE EXISTS (
        SELECT 1
        FROM studio_creates_movie scm
        JOIN studio s ON s.studio_id = scm.studio_id
        WHERE scm.movie_id = m.movie_id AND LOWER(s.name) LIKE LOWER(%s)
    )
    """
    params = (f"%{term}%",)
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")

# Additional search and utility functions for movies
# ...existing code...

# Function to get movie recommendations for a user
def get_reccomendations(username, limit):
    # Logic to fetch movie recommendations goes here
    pass