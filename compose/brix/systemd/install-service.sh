#!/bin/sh
sudo cp gunicorn-ip-local.service /etc/systemd/system
systemctl enable gunicorn-ip-local
systemctl daemon-reload
systemctl start gunicorn-ip-local
systemctl status gunicorn-ip-local
