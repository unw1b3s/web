<?php
final class Database {
    private PDO $pdo;
    public function __construct() {
        $this->pdo = new PDO('mysql:host='.(getenv('DB_HOST') ?: '127.0.0.1').';port='.(getenv('DB_PORT') ?: '3308').';dbname='.(getenv('DB_NAME') ?: 'conferences').';charset=utf8mb4', getenv('DB_USER') ?: 'conference', getenv('DB_PASSWORD') ?: 'local_conference', [PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION, PDO::ATTR_EMULATE_PREPARES=>false, PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
    }
    public function query(string $sql, array $params=[]): PDOStatement {
        $stmt=$this->pdo->prepare($sql); $stmt->execute($params); return $stmt;
    }
    public function pdo(): PDO { return $this->pdo; }
}
