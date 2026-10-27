# Краткий офлайн-справочник PHP и MySQL
Я сохранил рабочие заметки для проверки без интернета. Фреймворк не использую: сервер написан на обычном PHP с PDO.

## PDO
Соединение задаётся строкой mysql:host=127.0.0.1;port=3308;dbname=conferences;charset=utf8mb4. Режим исключений позволяет увидеть SQLSTATE в журнале. Эмуляция подготовленных запросов отключена. Пользовательские значения передаются через execute([$value]), а не вставляются в SQL.

Пример: $stmt=$pdo->prepare('SELECT id FROM users WHERE login=?'); $stmt->execute([$login]);

## Пароли и вывод
password_hash($password, PASSWORD_DEFAULT) создаёт хеш; password_verify проверяет пароль. htmlspecialchars($text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') экранирует вывод в HTML. session_regenerate_id(true) обновляет идентификатор после входа.

## Чтение ошибок
SQLSTATE 23000 означает нарушение ограничения: в MySQL код 1062 — повтор уникального значения, 1452 — отсутствующий внешний ключ. PHP Warning Undefined array key означает чтение отсутствующего поля массива. Перед чтением обязательных данных нужны значения по умолчанию и проверка.

Команды: php -l public/index.php проверяет синтаксис; php --help показывает локальную справку; docker compose logs db показывает журнал MySQL; git log --oneline показывает историю исправлений.

Источники для заметок: https://www.php.net/manual/en/pdo.prepared-statements.php и https://dev.mysql.com/doc/refman/8.4/en/constraint-invalid-data.html. Заметки являются кратким пересказом, не полной копией руководств.
