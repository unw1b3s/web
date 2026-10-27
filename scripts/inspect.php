<?php
require __DIR__.'/../app/bootstrap.php';
$db=new Database();
$explain=$db->query('EXPLAIN SELECT a.id FROM applications a JOIN events e ON e.id=a.event_id JOIN statuses s ON s.id=a.status_id WHERE a.status_id=? ORDER BY a.created_at DESC',[1])->fetchAll();
$hash=$db->query("SELECT password_hash FROM users WHERE login='student'")->fetchColumn();
$info=['server'=>$db->query('SELECT VERSION()')->fetchColumn(),'driver'=>$db->pdo()->getAttribute(PDO::ATTR_DRIVER_NAME),'tables'=>$db->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN),'student_password_is_hash'=>$hash!=='Student123' && password_verify('Student123',$hash),'application_indexes'=>$db->query('SHOW INDEX FROM applications')->fetchAll(),'explain'=>$explain,'note'=>'На малой учебной таблице оптимизатор может выбрать полный просмотр; индексы доступны для роста данных.'];
echo json_encode($info,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT)."\n";
