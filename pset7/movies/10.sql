SELECT DISTINCT people.name
FROM people
INNER JOIN directors ON directors.person_id = people.id
INNER JOIN movies oN directors.movie_id = movies.id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating >= 9.0;