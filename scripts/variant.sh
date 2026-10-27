#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
exec env APP_THEME=workshop php -S 127.0.0.1:8081 -t public
