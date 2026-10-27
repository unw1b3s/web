CREATE TABLE users (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 login VARCHAR(40) NOT NULL UNIQUE,
 password_hash VARCHAR(255) NOT NULL,
 email VARCHAR(254) NOT NULL UNIQUE,
 phone VARCHAR(12) NOT NULL,
 role ENUM('participant','admin') NOT NULL DEFAULT 'participant'
) ENGINE=InnoDB;
CREATE TABLE events (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(160) NOT NULL,
 event_date DATETIME NOT NULL,
 location VARCHAR(160) NOT NULL,
 description TEXT NOT NULL,
 theme ENUM('conference','workshop') NOT NULL DEFAULT 'conference'
) ENGINE=InnoDB;
CREATE TABLE applications (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 user_id INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 status ENUM('new','assigned','completed') NOT NULL DEFAULT 'new',
 payment ENUM('card','invoice') NOT NULL,
 room ENUM('main','small','online') NOT NULL,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE KEY one_application(user_id,event_id),
 FOREIGN KEY(user_id) REFERENCES users(id),
 FOREIGN KEY(event_id) REFERENCES events(id)
) ENGINE=InnoDB;
