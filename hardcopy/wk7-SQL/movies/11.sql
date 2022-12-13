-- write a SQL query to list the titles of the five highest rated movies
-- (in order) that Chadwick Boseman starred in, starting with the highest rated.

SELECT title FROM movies JOIN ratings ON movies.id = ratings.movie_id
JOIN stars ON stars.movie_id = ratings.movie_id JOIN people ON people.id = stars. person_id
WHERE name = "Chadwick Boseman" ORDER BY rating DESC LIMIT 5;