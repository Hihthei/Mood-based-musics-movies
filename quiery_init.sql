use mood_based_mm;

CREATE TABLE Mood (
    moodName VARCHAR(10) Primary Key);

CREATE TABLE Content (
    contentID INT Primary Key auto_increment,
    title VARCHAR(50),
    author VARCHAR(50),
    isMusic BOOLEAN,
    INDEX idx_title (title),
    INDEX idx_author (author));

CREATE TABLE Playlist (
    playlistID INT Primary Key auto_increment,
    playlistName VARCHAR(20));

CREATE TABLE Users (
    userID INT Primary Key auto_increment,
    userName VARCHAR(20),
    hashPassword VARCHAR(255),
    moodName VARCHAR(10) References Mood(moodName));

CREATE TABLE UsersTaste (
    userID INT References Users(userID),
    contentID INT References Content(contentID),
    moodName VARCHAR(10) References Mood(moodName),
    Primary Key (userID, contentID),
    INDEX idx_userID (userID),
    INDEX idx_contentID (contentID));

CREATE TABLE UsersAuthorization(
    userID INT References Users(userID),
    playlistID INT References Playlist(playlistID),
    authorization BOOLEAN,
    Primary Key (userID, playlistID),
    INDEX idx_userID (userID));

CREATE TABLE ContentRelation(
    contentID INT References Content(contentID),
    playlistID INT References Playlist(playlistID),
    Primary Key (contentID, playlistID));
