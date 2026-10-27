<?php
final class Auth {
    public function __construct(private Database $db) {}
    public function user(): ?array {
        return isset($_SESSION['uid']) ? ($this->db->query('SELECT id,login,email,phone,role FROM users WHERE id=?',[$_SESSION['uid']])->fetch() ?: null) : null;
    }
    public function register(array $data): void {
        $data += ['login'=>'','password'=>'','email'=>'','phone'=>''];
        $errors=[];
        if (!preg_match('/^[a-zA-Z0-9_]{3,40}$/D',$data['login'])) $errors[]='Логин: 3–40 латинских букв, цифр или подчёркиваний.';
        if (mb_strlen($data['password'])<8 || strlen($data['password'])>72) $errors[]='Пароль: от 8 символов, не более 72 байт.';
        if (!filter_var($data['email'],FILTER_VALIDATE_EMAIL) || strlen($data['email'])>254) $errors[]='Введите корректную почту.';
        if (!preg_match('/^\+7[0-9]{10}$/D',$data['phone'])) $errors[]='Телефон: +7 и 10 цифр.';
        if ($errors) throw new DomainException(implode(' ',$errors));
        try { $this->db->query('INSERT INTO users(login,password_hash,email,phone) VALUES (?,?,?,?)',[$data['login'],password_hash($data['password'],PASSWORD_DEFAULT),$data['email'],$data['phone']]); }
        catch (PDOException $ex) { if ($ex->getCode()==='23000') throw new DomainException('Логин или почта уже заняты.'); throw $ex; }
    }
    public function login(string $login,string $password): void {
        if (($_SESSION['attempts'] ?? 0)>=5 && time()-($_SESSION['last_attempt'] ?? 0)<60) throw new DomainException('Слишком много попыток. Подождите минуту.');
        $user=$this->db->query('SELECT * FROM users WHERE login=?',[$login])->fetch();
        if (!$user || !password_verify($password,$user['password_hash'])) {
            $_SESSION['attempts']=($_SESSION['attempts'] ?? 0)+1; $_SESSION['last_attempt']=time();
            throw new DomainException('Неверный логин или пароль.');
        }
        session_regenerate_id(true); $_SESSION['uid']=$user['id']; $_SESSION['attempts']=0; $_SESSION['csrf']=bin2hex(random_bytes(32));
    }
}
