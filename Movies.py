from db import get_connection

# globals to remember the last search
last_where = None
last_params = None


def print_movies(rows):
    if not rows:
        print("No movies found.")
        return None
    print("\nResults:")
    for movie_id, title, length, mpaa, cast_names, director_names, avg_user_rating in rows:
        h, m = divmod((length or 0), 60)
        cast_str = cast_names or "N/A"
        dir_str = director_names or "N/A"
        user_str = f"{avg_user_rating:.1f}" if avg_user_rating is not None else "N/A"
        print(
            f"{movie_id}: {title}\n"
            f"  Cast: {cast_str}\n"
            f"  Director: {dir_str}\n"
            f"  Length: {h}h {m}m\n"
            f"  Ratings: MPAA={mpaa or 'N/A'}, User(avg)={user_str}\n"
        )
    return 1


def get_movies(where_sql: str, params: tuple, order_sql: str = "m.title ASC"):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                WITH cast_agg AS (
                    SELECT
                        m.movie_id,
                        COALESCE(string_agg(DISTINCT c_cast.name, ', '), '') AS cast_names,
                        COALESCE(string_agg(DISTINCT c_dir.name,  ', '), '') AS director_names
                    FROM movie m
                    LEFT JOIN contributor_acts_movie cam
                        ON cam.movie_id = m.movie_id
                    LEFT JOIN contributor c_cast
                        ON c_cast.con_id = cam.con_id
                    LEFT JOIN contributor_directs_movie cdm
                        ON cdm.mov_id = m.movie_id
                    LEFT JOIN contributor c_dir
                        ON c_dir.con_id = cdm.con_id
                    GROUP BY m.movie_id
                ),
                rating_agg AS (
                    SELECT
                        ur.movie_id,
                        ROUND(AVG(ur.star_rating)::numeric, 1) AS avg_rating
                    FROM user_rates_movie ur
                    GROUP BY ur.movie_id
                )
                SELECT
                    m.movie_id,
                    m.title,
                    m.length,
                    m.age_rating,
                    NULLIF(ca.cast_names, '')      AS cast_names,
                    NULLIF(ca.director_names, '')  AS director_names,
                    ra.avg_rating                   AS avg_user_rating
                FROM movie m
                LEFT JOIN cast_agg   ca USING (movie_id)
                LEFT JOIN rating_agg ra USING (movie_id)
                {where_sql}
                ORDER BY {order_sql};
                """,
                params,
            )
            rows = cur.fetchall()
            print_movies(rows)
            return rows
    except Exception as e:
        print("Error fetching movies:", e)
        return []
    finally:
        conn.close()
        server.stop()


# ---------- SEARCH FUNCTIONS ----------
def search_movie_title(term: str):
    global last_where, last_params
    where = "WHERE LOWER(m.title) LIKE LOWER(%s)"
    params = (f"%{term}%",)
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")


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


def search_movie_genre(term: str):
    global last_where, last_params
    where = """
    WHERE EXISTS (
        SELECT 1
        FROM movie_has_genre mg
        JOIN genre g ON g.genre_id = mg.genre_id
        WHERE mg.movie_id = m.movie_id AND LOWER(g.name) LIKE LOWER(%s)
    )
    """
    params = (f"%{term}%",)
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")


def search_movie_length(term: str):
    global last_where, last_params
    term = term.strip()
    if "-" in term:
        lo, hi = [int(x.strip()) for x in term.split("-", 1)]
        where = "WHERE m.length BETWEEN %s AND %s"
        params = (lo, hi)
        order = "m.length ASC, m.title ASC"
    else:
        max_len = int(term)
        where = "WHERE m.length <= %s"
        params = (max_len,)
        order = "m.length ASC, m.title ASC"
    last_where, last_params = where, params
    return get_movies(where, params, order_sql=order)


def search_movie_release(term: str):
    global last_where, last_params
    year = int(term.strip())
    where = "WHERE m.release_year = %s"
    params = (year,)
    last_where, last_params = where, params
    return get_movies(where, params, order_sql="m.title ASC, m.release_year ASC")


# ---------- SORTING FUNCTIONS ----------
def sort_movies(order_by: str, ascending=True):

    global last_where, last_params
    if not last_where or not last_params:
        print("No previous search found to sort.")
        return []

    direction = "ASC" if ascending else "DESC"

    if order_by == "title":
        order_sql = f"m.title {direction}, m.release_year {direction}"
    elif order_by == "studio":
        order_sql = f"(SELECT s.name FROM studio_creates_movie scm JOIN studio s ON s.studio_id = scm.studio_id WHERE scm.movie_id = m.movie_id LIMIT 1) {direction}, m.title ASC"
    elif order_by == "genre":
        order_sql = f"(SELECT g.name FROM movie_has_genre mg JOIN genre g ON g.genre_id = mg.genre_id WHERE mg.movie_id = m.movie_id LIMIT 1) {direction}, m.title ASC"
    elif order_by == "year":
        order_sql = f"m.release_year {direction}, m.title ASC"
    else:
        print("Invalid sort option.")
        return []

    return get_movies(last_where, last_params, order_sql=order_sql)


def mark_movie_as_watched(username, movie_id):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_watches_movie (username, movie_id, date)
                VALUES (%s, %s, NOW());
            """, (username, movie_id))
            conn.commit()
            print(f"{username} watched movie ID {movie_id}.")
    except Exception as e:
        print("Error marking movie as watched:", e)
    finally:
        conn.close()
        server.stop()


def movie_exists(movie_id):
    conn, server = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM movie WHERE movie_id = %s;", (movie_id,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print("Error checking movie existence:", e)
        return False
    finally:
        conn.close()
        server.stop()
