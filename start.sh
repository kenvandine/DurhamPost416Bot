#!/bin/bash
set -e

APP_ID=$(snapctl get app-id)
BOT_TOKEN=$(snapctl get bot-token)

if [ -z "$APP_ID" ]; then
    echo "APP_ID required"
    exit 1
fi

if [ -z "$BOT_TOKEN" ]; then
    echo "BOT_TOKEN required"
    exit 1
fi

export APP_ID BOT_TOKEN
python3 $SNAP/bin/app.py "$@"
