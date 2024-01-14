CREATE DATABASE students;
CREATE USER 'root2'@'localhost' IDENTIFIED BY 'Nik1701';
GRANT ALL PRIVILEGES ON students.* TO 'root2'@'localhost';
FLUSH PRIVILEGES;

USE students;
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(50) UNIQUE NOT NULL,
    address VARCHAR(100)
);

SHOW TABLES;
DESCRIBE student;
SELECT * FROM student;
