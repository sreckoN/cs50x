SELECT movies.title
FROM movies
INNER JOIN stars ON stars.movie_id = movies.id
INNER JOIN people ON stars.person_id = people.id
WHERE people.name = 'Johnny Depp' AND movies.id IN (SELECT movies.id
                                                    FROM movies
                                                    INNER JOIN stars ON stars.movie_id = movies.id
                                                    INNER JOIN people ON stars.person_id = people.id
                                                    WHERE people.name = 'Helena Bonham Carter');