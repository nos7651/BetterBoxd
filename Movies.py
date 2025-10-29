from db import get_connection


def print_movies(rows):
    if not rows:
        print("No movies found.")
        return
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
    except Exception as e:
        print("Error fetching movies:", e)
    finally:
        conn.close()
        server.stop()



def search_movie_title(term: str):
    where = "WHERE LOWER(m.title) LIKE LOWER(%s)"
    params = (f"%{term}%",)
    get_movies(where, params, order_sql="m.title ASC")

def search_movie_cast(term: str):

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
    get_movies(where, params, order_sql="m.title ASC")

def search_movie_studio(term: str):
    where = """
    WHERE EXISTS (
        SELECT 1
        FROM studio_creates_movie scm
        JOIN studio s ON s.studio_id = scm.studio_id
        WHERE scm.movie_id = m.movie_id AND LOWER(s.name) LIKE LOWER(%s)
    )
    """
    params = (f"%{term}%",)
    get_movies(where, params, order_sql="m.title ASC")

def search_movie_genre(term: str):
    where = """
    WHERE EXISTS (
        SELECT 1
        FROM movie_has_genre mg
        JOIN genre g ON g.genre_id = mg.genre_id
        WHERE mg.movie_id = m.movie_id AND LOWER(g.name) LIKE LOWER(%s)
    )
    """
    params = (f"%{term}%",)
    get_movies(where, params, order_sql="m.title ASC")

def search_movie_length(term: str):
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
    get_movies(where, params, order_sql=order)

def search_movie_release(term: str):
    year = int(term.strip())

    where = "WHERE m.release_year = %s"
    params = (year,)

    get_movies(where, params, order_sql="m.title ASC")
