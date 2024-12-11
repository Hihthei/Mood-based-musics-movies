use mood_based_mm;

INSERT INTO mood
values 
	('happy'),
	('chill'),
	('sad');

INSERT INTO Content (title, author, isMusic, moodName)
VALUES
    ('Inception', 'Christopher Nolan', 0, "chill"),
    ('Bohemian Rhapsody', 'Queen', 1, "sad"),
    ('The Dark Knight', 'Christopher Nolan', 0, "happy"),
    ('Imagine', 'John Lennon', 1, "chill"),
    ('The Godfather', 'Francis Ford Coppola', 0, "happy"),
    ('Smells Like Teen Spirit', 'Nirvana', 1, "chill"),
    ('Pulp Fiction', 'Quentin Tarantino', 0, "sad"),
    ('Shape of You', 'Ed Sheeran', 1, "sad"),sad
    ('Fight Club', 'David Fincher', 0, "chill"),
    ('Rolling in the Deep', 'Adele', 1, "happy"),
    ('Forrest Gump', 'Robert Zemeckis', 0, "sad"),
    ('Like a Rolling Stone', 'Bob Dylan', 1, "chill"),
    ('The Shawshank Redemption', 'Frank Darabont', 0, "sad"),
    ('Stairway to Heaven', 'Led Zeppelin', 1, "sad"),
    ('The Matrix', 'Lana and Lilly Wachowski', 0, "happy"),
    ('Sweet Child O Mine', 'Guns N Roses', 1, "chill"),
    ('Gladiator', 'Ridley Scott', 0, "happy"),
    ('Hotel California', 'Eagles', 1, "chill"),
    ('Star Wars: A New Hope', 'George Lucas', 0, "happy"),
    ('Hey Jude', 'The Beatles', 1, "sad");