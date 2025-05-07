#!/bin/bash
set -e

APP_ID=$(snapctl get app_id)
BOT_TOKEN=$(snapctl get bot_token)

if [ -n "$APP_ID" ]; then
    echo "APP_ID required"
    exit 1
fi

if [ -n "$BOT_TOKEN" ]; then
    echo "BOT_TOKEN required"
    exit 1
fi

export APP_ID BOT_TOKEN
python3 $SNAP/bin/app.py "$@"
