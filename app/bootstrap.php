<?php
declare(strict_types=1);
date_default_timezone_set('Europe/Moscow');
foreach (file_exists(__DIR__.'/../.env') ? file(__DIR__.'/../.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) : [] as $line) {
    if (!str_starts_with(trim($line), '#') && str_contains($line, '=')) {
        [$key, $value] = explode('=', $line, 2);
        if (getenv(trim($key)) === false) putenv(trim($key).'='.trim($value));
    }
}
spl_autoload_register(function ($class) { require __DIR__.'/src/'.$class.'.php'; });
function e(mixed $value): string { return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
