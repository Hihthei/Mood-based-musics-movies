use mood_based_mm;

INSERT INTO mood
values 
	('happy'),
	('chill'),
	('sad');

INSERT INTO users (userName, hashPassword, moodName)
VALUES
	('TinyChoice', 'password', 'happy'),
    ('Celin', 'Celin', 'sad'),
    ('Nico', 'Nico', 'chill'),
    ('Loan', 'Loan', 'happy');

INSERT INTO Content (title, author, isMusic)
VALUES
    ('Inception', 'Christopher Nolan', 0),
    ('Bohemian Rhapsody', 'Queen', 1),
    ('The Dark Knight', 'Christopher Nolan', 0),
    ('Imagine', 'John Lennon', 1),
    ('The Godfather', 'Francis Ford Coppola', 0),
    ('Smells Like Teen Spirit', 'Nirvana', 1),
    ('Pulp Fiction', 'Quentin Tarantino', 0),
    ('Shape of You', 'Ed Sheeran', 1),
    ('Fight Club', 'David Fincher', 0),
    ('Rolling in the Deep', 'Adele', 1),
    ('Forrest Gump', 'Robert Zemeckis', 0),
    ('Like a Rolling Stone', 'Bob Dylan', 1),
    ('The Shawshank Redemption', 'Frank Darabont', 0),
    ('Stairway to Heaven', 'Led Zeppelin', 1),
    ('The Matrix', 'Lana and Lilly Wachowski', 0),
    ('Sweet Child O Mine', 'Guns N Roses', 1),
    ('Gladiator', 'Ridley Scott', 0),
    ('Hotel California', 'Eagles', 1),
    ('Star Wars: A New Hope', 'George Lucas', 0),
    ('Hey Jude', 'The Beatles', 1);

INSERT INTO Playlist (playlistName)
VALUES ('test');

INSERT INTO UsersAuthorization
SELECT userID, playlistID, 1
FROM Users, Playlist
WHERE Users.userName = 'Nico' AND Playlist.playlistName = 'test';

INSERT INTO UsersTaste
VALUES
    (1, 1, 'chill'),
    (2, 1, 'chill'),
    (3, 1, 'happy'),
    (3, 3, 'happy'),
    (3, 5, 'chill'),
    (3, 7, 'sad'),
    (3, 9, 'happy'),
    (3, 11, 'sad'),
    (3, 13, 'chill'),
    (3, 15, 'sad'),
    (3, 17, 'chill');



SELECT content.title, moodName
FROM (
    SELECT contentID, moodName, COUNT(*) AS mood_count,
           RANK() OVER (PARTITION BY contentID ORDER BY COUNT(*) DESC) AS rang
    FROM UsersTaste
    GROUP BY contentID, moodName
) AS ranked_moods, content
WHERE rang = 1 and content.contentID = ranked_moods.contentID;