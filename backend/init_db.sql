-- Run this once against your MySQL server:
--   mysql -u root -p < init_db.sql
CREATE DATABASE IF NOT EXISTS mood_music CHARACTER SET utf8mb4;
USE mood_music;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mood_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    mood VARCHAR(32) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (session_id)
);

CREATE TABLE IF NOT EXISTS preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    language VARCHAR(64),
    region VARCHAR(8),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (session_id)
);

CREATE TABLE IF NOT EXISTS playlist_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    mood VARCHAR(32) NOT NULL,
    language VARCHAR(64),
    region VARCHAR(8),
    playlist_id VARCHAR(64),
    playlist_name VARCHAR(255),
    spotify_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (session_id)
);
USE mood_music;
SELECT * FROM users;
SELECT * FROM preferences;