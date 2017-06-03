#!/bin/sh
sudo systemctl stop gunicorn-ip-local
sudo cp gunicorn-ip-local.service /etc/systemd/system
sudo systemctl enable gunicorn-ip-local
sudo systemctl daemon-reload
sudo systemctl start gunicorn-ip-local
sudo systemctl status gunicorn-ip-local
