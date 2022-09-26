-- write a SQL query to list the titles of all movies in which both
-- Johnny Depp and Helena Bonham Carter starred.

SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE name = "Johnny Depp" AND movies.title IN
(SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE name = "Helena Bonham Carter");