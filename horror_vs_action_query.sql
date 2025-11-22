
WITH users_with_10plus_horror AS (
    SELECT uwm.username
    FROM user_watches_movie uwm
    JOIN movie_has_genre mhg ON uwm.movie_id = mhg.movie_id
    JOIN genre g ON mhg.genre_id = g.genre_id
    WHERE LOWER(g.name) = 'horror'
    GROUP BY uwm.username
    HAVING COUNT(DISTINCT uwm.movie_id) > 10
),


horror_ratings AS (
    SELECT
        'Horror' AS genre,
        AVG(urm.star_rating) AS avg_rating
    FROM user_rates_movie urm
    JOIN movie_has_genre mhg ON urm.movie_id = mhg.movie_id
    JOIN genre g ON mhg.genre_id = g.genre_id
    WHERE LOWER(g.name) = 'horror'
      AND urm.username IN (SELECT username FROM users_with_10plus_horror)
),


action_ratings AS (
    SELECT
        'Action' AS genre,
        AVG(urm.star_rating) AS avg_rating
    FROM user_rates_movie urm
    JOIN movie_has_genre mhg ON urm.movie_id = mhg.movie_id
    JOIN genre g ON mhg.genre_id = g.genre_id
    WHERE LOWER(g.name) = 'action'
      AND urm.username IN (SELECT username FROM users_with_10plus_horror)
)

SELECT genre, avg_rating
FROM horror_ratings
UNION ALL
SELECT genre, avg_rating
FROM action_ratings;
