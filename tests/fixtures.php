<?php
require __DIR__.'/../app/bootstrap.php';
$db=new Database();
// Данные только для локальных проверок; повторный запуск не создаёт копий.
foreach (['student','reviewer','other'] as $login) {
    if (!$db->query('SELECT id FROM users WHERE login=?',[$login])->fetch()) $db->query('INSERT INTO users(login,password_hash,email,phone) VALUES (?,?,?,?)',[$login,password_hash('Student123',PASSWORD_DEFAULT),$login.'@example.ru','+79991234567']);
}
foreach (['conference','workshop'] as $theme) {
    $past=$db->query('SELECT id FROM events WHERE theme=? AND event_date<NOW() LIMIT 1',[$theme])->fetchColumn();
    $uid=$db->query('SELECT id FROM users WHERE login=?',['student'])->fetchColumn();
    $db->query('INSERT IGNORE INTO applications(user_id,event_id,payment,room,status_id) VALUES (?,?,?,?,3)',[$uid,$past,'card','main']);
    $uid=$db->query('SELECT id FROM users WHERE login=?',['reviewer'])->fetchColumn();
    $db->query('INSERT IGNORE INTO applications(user_id,event_id,payment,room,status_id) VALUES (?,?,?,?,1)',[$uid,$past,'invoice','small']);
}
$db->query("DELETE r FROM reviews r JOIN applications a ON a.id=r.application_id JOIN users u ON u.id=a.user_id WHERE u.login='reviewer'");
$db->query("UPDATE applications a JOIN users u ON u.id=a.user_id SET a.status_id=1 WHERE u.login='reviewer'");
echo "Fixtures ready\n";
