<?php
final class Portal {
    public function __construct(private Database $db, private string $theme) {}
    public function events(): array { return $this->db->query('SELECT * FROM events WHERE theme=? ORDER BY event_date',[$this->theme])->fetchAll(); }
    public function apply(int $user,int $event,string $payment,string $room): void {
        if (!in_array($payment,['card','invoice'],true) || !in_array($room,['main','small','online'],true)) throw new DomainException('Выберите оплату и помещение из списка.');
        $item=$this->db->query('SELECT * FROM events WHERE id=? AND theme=?',[$event,$this->theme])->fetch();
        if (!$item || strtotime($item['event_date'])<=time()) throw new DomainException('Приём заявок на это мероприятие закрыт.');
        try { $this->db->query('INSERT INTO applications(user_id,event_id,payment,room) VALUES (?,?,?,?)',[$user,$event,$payment,$room]); }
        catch (PDOException $ex) { if ($ex->getCode()==='23000') throw new DomainException('Вы уже подали заявку на это мероприятие.'); throw $ex; }
    }
    public function applications(array $user,int $status=0): array {
        $sql='SELECT a.*,e.title,e.event_date,e.location,u.login,s.name status_name,r.body,r.rating FROM applications a JOIN events e ON e.id=a.event_id JOIN users u ON u.id=a.user_id JOIN statuses s ON s.id=a.status_id LEFT JOIN reviews r ON r.application_id=a.id WHERE e.theme=?';
        $params=[$this->theme];
        if ($user['role']!=='admin') { $sql.=' AND a.user_id=?'; $params[]=$user['id']; }
        if ($status) { $sql.=' AND a.status_id=?'; $params[]=$status; }
        return $this->db->query($sql.' ORDER BY a.created_at DESC,a.id DESC',$params)->fetchAll();
    }
    public function changeStatus(int $id,int $status): void {
        $app=$this->db->query('SELECT a.*,e.event_date FROM applications a JOIN events e ON e.id=a.event_id WHERE a.id=? AND e.theme=?',[$id,$this->theme])->fetch();
        if (!$app || $status!==(int)$app['status_id']+1 || $status>3) throw new DomainException('Разрешён только следующий статус.');
        if ($status===3 && strtotime($app['event_date'])>time()) throw new DomainException('Мероприятие ещё не завершилось.');
        $this->db->query('UPDATE applications SET status_id=? WHERE id=? AND status_id=?',[$status,$id,$app['status_id']]);
    }
    public function review(int $user,int $id,string $body,int $rating): void {
        if (mb_strlen(trim($body))<5 || mb_strlen($body)>1000 || $rating<1 || $rating>5) throw new DomainException('Отзыв: 5–1000 символов, оценка от 1 до 5.');
        $app=$this->db->query('SELECT a.id FROM applications a JOIN events e ON e.id=a.event_id WHERE a.id=? AND a.user_id=? AND a.status_id=3 AND e.event_date<=NOW() AND e.theme=?',[$id,$user,$this->theme])->fetch();
        if (!$app) throw new DomainException('Отзыв доступен только владельцу завершённой заявки после мероприятия.');
        try { $this->db->query('INSERT INTO reviews(application_id,body,rating) VALUES (?,?,?)',[$id,trim($body),$rating]); }
        catch (PDOException $ex) { if ($ex->getCode()==='23000') throw new DomainException('Отзыв уже оставлен.'); throw $ex; }
    }
    public function cancel(int $user,int $id): void {
        $stmt=$this->db->query('DELETE a FROM applications a JOIN events e ON e.id=a.event_id WHERE a.id=? AND a.user_id=? AND a.status_id=1 AND e.theme=?',[$id,$user,$this->theme]);
        if (!$stmt->rowCount()) throw new DomainException('Можно удалить только свою новую заявку.');
    }
}
