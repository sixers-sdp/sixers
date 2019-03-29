#!/usr/bin/env bash

echo "Pulling latest repo on EV3"
ssh ev3 bash -c "cd sixers;git pull"

echo "Restarting ev3 systemd service"

ssh ev3_root bash -c "systemctl daemon-reload"
ssh ev3_root bash -c "systemctl restart ev3.service"


echo "Pulling on rpi"

ssh rpi bash -c "cd sixers;git pull"

echo "restarting systemd service on rpi"

ssh rpi_root bash -c "systemctl daemon-reload"
ssh rpi_root bash -c "systemctl restart albert.service"
