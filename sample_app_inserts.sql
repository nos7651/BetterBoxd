-- Sample app inserts for demonstration purposes
-- User creation, watching movies, rating, following, playlist creation.

INSERT INTO app_user (username, password, email, first_name, last_name, creation_date, last_access_ts)
VALUES ('alice', 'pass123', 'alice@gmail.com', 'Alice', 'Brown', NOW(), NOW()),
       ('bob', 'qwerty', 'bob@gmail.com', 'Bob', 'Smith', NOW(), NOW());

INSERT INTO movie (title, length, age_rating)
VALUES ('Neon Tide', 120, 'PG-13'), ('Midnight Code', 105, 'R');

INSERT INTO user_watches_movie (username, movie_id, date)
VALUES ('alice', 1, NOW()), ('bob', 2, NOW());

INSERT INTO user_rates_movie (username, movie_id, star_rating)
VALUES ('alice', 1, 4.5), ('bob', 2, 3.0);

INSERT INTO playlist (playlist_name)
VALUES ('Favorites'), ('Watch Later');

INSERT INTO user_creates_playlist (playlist_id, username)
VALUES (1, 'alice'), (2, 'bob');

INSERT INTO playlist_contains_movie (playlist_id, movie_id, times_watched)
VALUES (1, 1, 5), (2, 2, 3);

INSERT INTO user_follows_user (followed_username, follower_username)
VALUES ('alice', 'bob');
