<?php
require __DIR__.'/../app/bootstrap.php';
$db=new Database();
$db->query('CREATE TABLE IF NOT EXISTS schema_migrations (name VARCHAR(100) PRIMARY KEY)');
foreach (['001_initial.sql','migrations/002_statuses_reviews.sql'] as $file) {
    if ($db->query('SELECT name FROM schema_migrations WHERE name=?',[$file])->fetch()) continue;
    $db->pdo()->exec(file_get_contents(__DIR__.'/../database/'.$file));
    $db->query('INSERT INTO schema_migrations VALUES (?)',[$file]);
    echo "Applied $file\n";
}
foreach ([['admin','Admin12345','admin'],['student','Student123','participant']] as [$login,$password,$role]) {
    if (!$db->query('SELECT id FROM users WHERE login=?',[$login])->fetch()) $db->query('INSERT INTO users(login,password_hash,email,phone,role) VALUES (?,?,?,?,?)',[$login,password_hash($password,PASSWORD_DEFAULT),$login.'@example.ru','+79991234567',$role]);
}
if (!$db->query('SELECT id FROM events LIMIT 1')->fetch()) {
    foreach ([['Веб-разработка: первые шаги','2027-03-15 10:00:00','Москва, Технопарк','Практическая конференция о создании сайтов. Обсудим HTML, PHP и работу с базами данных.','conference'],['Дизайн цифровых продуктов','2027-04-20 11:00:00','Санкт-Петербург, Лекторий','Понятные интерфейсы, доступность и адаптивная вёрстка.','conference'],['Технологии и образование','2026-09-10 12:00:00','Казань, ИТ-парк','Завершившаяся встреча о технологиях обучения.','conference'],['Основы керамики','2027-05-12 12:00:00','Москва, Студия № 2','Практическая работа с глиной и создание первой чашки.','workshop'],['Акварельный пейзаж','2026-09-12 12:00:00','Казань, Мастерская','Завершившийся мастер-класс по акварели.','workshop']] as $event) $db->query('INSERT INTO events(title,event_date,location,description,theme) VALUES (?,?,?,?,?)',$event);
}
echo 'Database: '.$db->query('SELECT VERSION()')->fetchColumn()."\n";
