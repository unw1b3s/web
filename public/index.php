<?php
require __DIR__.'/../app/bootstrap.php';
ini_set('display_errors','0');
ini_set('session.use_strict_mode','1');
session_set_cookie_params(['httponly'=>true,'secure'=>!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS']!=='off','samesite'=>'Lax']);
session_start();
header("Content-Security-Policy: default-src 'self'; style-src 'self'; script-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
header('X-Content-Type-Options: nosniff'); header('Referrer-Policy: same-origin'); header('Cache-Control: no-store');
if (isset($_SESSION['active']) && time()-$_SESSION['active']>1800) { $_SESSION=[]; session_regenerate_id(true); }
$_SESSION['active']=time(); $_SESSION['csrf'] ??= bin2hex(random_bytes(32));
$theme=getenv('APP_THEME')==='workshop' ? 'workshop' : 'conference';
$title=$theme==='workshop' ? 'Мастерские.РФ' : 'Конференции.РФ';
$page=is_string($_GET['page'] ?? null) ? $_GET['page'] : 'events';
if (!in_array($page,['events','register','login','account','apply','applications','admin'],true)) { http_response_code(404); $page='missing'; } $error=''; $notice=$_SESSION['notice'] ?? ''; unset($_SESSION['notice']);
function redirect(string $page): never { header('Location: /?page='.$page); exit; }
function csrf(): string { return '<input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'">'; }
try {
    $db=new Database(); $auth=new Auth($db); $portal=new Portal($db,$theme); $user=$auth->user();
    if ($_SERVER['REQUEST_METHOD']==='POST') {
        if (!is_string($_POST['csrf'] ?? null) || !hash_equals($_SESSION['csrf'],$_POST['csrf'])) { http_response_code(403); throw new DomainException('Форма устарела. Обновите страницу.'); }
        foreach ($_POST as $value) if (!is_string($value)) throw new DomainException('Некорректные данные формы.');
        $action=$_POST['action'] ?? '';
        if ($action==='register') { $auth->register(array_map('trim',array_intersect_key($_POST,array_flip(['login','email','phone'])))+['password'=>$_POST['password'] ?? '']); $_SESSION['notice']='Регистрация завершена. Войдите в личный кабинет.'; redirect('login'); }
        elseif ($action==='login') { $auth->login(trim($_POST['login'] ?? ''),$_POST['password'] ?? ''); redirect('account'); }
        else {
            if (!$user) { http_response_code(403); throw new DomainException('Необходима авторизация.'); }
            if ($action==='logout') { $_SESSION=[]; session_regenerate_id(true); redirect('events'); }
            elseif ($action==='status') { if ($user['role']!=='admin') { http_response_code(403); throw new DomainException('Доступ запрещён.'); } $portal->changeStatus((int)($_POST['id'] ?? 0),(int)($_POST['status'] ?? 0)); }
            else {
                if ($user['role']!=='participant') { http_response_code(403); throw new DomainException('Действие доступно участнику.'); }
                if ($action==='apply') $portal->apply($user['id'],(int)($_POST['event'] ?? 0),$_POST['payment'] ?? '',$_POST['room'] ?? '');
                elseif ($action==='review') $portal->review($user['id'],(int)($_POST['id'] ?? 0),$_POST['body'] ?? '',(int)($_POST['rating'] ?? 0));
                elseif ($action==='cancel') $portal->cancel($user['id'],(int)($_POST['id'] ?? 0));
                else throw new DomainException('Неизвестное действие.');
            }
            $_SESSION['notice']='Изменения сохранены.'; redirect($user['role']==='admin' ? 'admin' : 'applications');
        }
    }
} catch (DomainException $ex) { $error=$ex->getMessage(); }
catch (Throwable $ex) { error_log((string)$ex); http_response_code(500); $error='Не удалось выполнить запрос. Попробуйте позже.'; }
if (in_array($page,['account','applications','apply','admin'],true) && empty($user)) { if ($_SERVER['REQUEST_METHOD']!=='POST') redirect('login'); $page='login'; }
if ($page==='admin' && ($user['role'] ?? '')!=='admin') { http_response_code(403); $error='Доступ запрещён.'; $page='denied'; }
$events=isset($portal) ? $portal->events() : [];
require __DIR__.'/../app/templates/layout.php';
