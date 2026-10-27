CREATE TABLE statuses (
 id TINYINT UNSIGNED PRIMARY KEY,
 code VARCHAR(20) NOT NULL UNIQUE,
 name VARCHAR(30) NOT NULL
) ENGINE=InnoDB;
INSERT INTO statuses VALUES (1,'new','Новая'),(2,'assigned','Назначено'),(3,'completed','Завершено');
ALTER TABLE applications ADD status_id TINYINT UNSIGNED NULL;
UPDATE applications a JOIN statuses s ON s.code=a.status SET a.status_id=s.id;
ALTER TABLE applications MODIFY status_id TINYINT UNSIGNED NOT NULL DEFAULT 1,
 ADD CONSTRAINT fk_status FOREIGN KEY(status_id) REFERENCES statuses(id),
 ADD INDEX status_created(status_id,created_at),
 DROP COLUMN status;
CREATE TABLE reviews (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 application_id INT UNSIGNED NOT NULL UNIQUE,
 body TEXT NOT NULL,
 rating TINYINT UNSIGNED NOT NULL,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT valid_rating CHECK(rating BETWEEN 1 AND 5),
 FOREIGN KEY(application_id) REFERENCES applications(id) ON DELETE CASCADE
) ENGINE=InnoDB;
