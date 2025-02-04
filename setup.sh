#!/bin/bash

echo "[+] Building Database [+]"
flask db init || true
flask db migrate
flask db upgrade

echo "[+] Start app [+]"
python3 app.py runserver
