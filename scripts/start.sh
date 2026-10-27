#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
[ -f .env ] || cp .env.example .env
docker compose up -d --wait
php scripts/setup.php
python3 scripts/build.py
exec php -S 127.0.0.1:8080 -t public
