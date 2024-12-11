create database mood_based_mm;

use mood_based_mm;

CREATE TABLE Mood (
    moodName VARCHAR(10) Primary Key);

CREATE TABLE Content (
    contentID INT Primary Key auto_increment,
    moodName VARCHAR(10) References Mood(moodName),
    title VARCHAR(50),
    author VARCHAR(50),
    isMusic BOOLEAN,
    INDEX idx_title (title),
    INDEX idx_author (author));

CREATE TABLE Playlist (
    playlistID INT Primary Key auto_increment,
    playlistName VARCHAR(20)),
    INDEX idx_playlistName (playlistName);

CREATE TABLE Users (
    userID INT Primary Key auto_increment,
    userName VARCHAR(20),
    hashPassword VARCHAR(255),
    moodName VARCHAR(10) References Mood(moodName),
    INDEX idx_userName (userName));

CREATE TABLE UsersTaste (
    userID INT References Users(userID),
    contentID INT References Content(contentID),
    moodName VARCHAR(10) References Mood(moodName),
    Primary Key (userID, contentID),
    INDEX idx_moodName (moodName));

CREATE TABLE UsersAuthorization(
    userID INT References Users(userID),
    playlistID INT References Playlist(playlistID),
    authorization BOOLEAN,
    Primary Key (userID, playlistID),
    INDEX idx_authorization (authorization));

CREATE TABLE ContentRelation(
    contentID INT References Content(contentID),
    playlistID INT References Playlist(playlistID),
    Primary Key (contentID, playlistID));

CREATE VIEW global_taste as
    SELECT c.title, c.author, COALESCE(um.moodName, c.moodName) AS moodName, c.isMusic, c.contentID
    FROM content c
    LEFT OUTER JOIN (
        SELECT um.contentID, um.moodName, 
            RANK() OVER (PARTITION BY um.contentID ORDER BY COUNT(*) DESC) AS rang
        FROM userstaste um
        GROUP BY um.contentID, um.moodName
    ) um ON c.contentID = um.contentID
    where um.rang = 1 or um.rang is null;

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