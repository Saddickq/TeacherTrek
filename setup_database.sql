CREATE DATABASE IF NOT EXISTS teacher_database;
USE teacher_database;
CREATE USER IF NOT EXISTS 'teacher'@'localhost' IDENTIFIED BY 'teachertrek';
GRANT ALL PRIVILEGES ON teacher_database.* TO 'teacher'@'localhost';
