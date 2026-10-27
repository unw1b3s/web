<?php
require __DIR__.'/../app/bootstrap.php';
$db=new Database();
$db->pdo()->exec(file_get_contents(__DIR__.'/../database/001_initial.sql'));
$db->query("INSERT INTO users(login,password_hash,email,phone) VALUES ('migration_user','hash','migration@example.ru','+79991234567')");
$db->query("INSERT INTO events(title,event_date,location,description) VALUES ('Проверка миграции','2026-01-01','Москва','Тест')");
$db->query("INSERT INTO applications(user_id,event_id,status,payment,room) VALUES (1,1,'assigned','card','main')");
$before=$db->query('SELECT id,user_id,event_id,status FROM applications')->fetch();
$db->pdo()->exec(file_get_contents(__DIR__.'/../database/migrations/002_statuses_reviews.sql'));
$after=$db->query('SELECT a.id,user_id,event_id,s.code status FROM applications a JOIN statuses s ON s.id=a.status_id')->fetch();
$checks=['legacy_row_preserved'=>$before===$after];
try {$db->query("INSERT INTO applications(user_id,event_id,payment,room,status_id) VALUES (999,1,'card','main',1)");$checks['foreign_key']=false;}catch(PDOException $e){$checks['foreign_key']=$e->errorInfo[1]===1452;}
try {$db->query("INSERT INTO reviews(application_id,body,rating) VALUES (1,'Тест',6)");$checks['rating_check']=false;}catch(PDOException $e){$checks['rating_check']=true;}
$checks['no_orphans']=(int)$db->query('SELECT COUNT(*) FROM applications a LEFT JOIN users u ON u.id=a.user_id LEFT JOIN events e ON e.id=a.event_id LEFT JOIN statuses s ON s.id=a.status_id WHERE u.id IS NULL OR e.id IS NULL OR s.id IS NULL')->fetchColumn()===0;
echo json_encode(['server'=>$db->query('SELECT VERSION()')->fetchColumn(),'before'=>$before,'after'=>$after,'checks'=>$checks],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
exit(in_array(false,$checks,true) ? 1 : 0);
