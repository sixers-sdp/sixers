#!/usr/bin/env bash

ssh ev3 bash -c "cd sixers;git pull"
ssh ev3_root bash -c "systemctl daemon-reload"
ssh ev3_root bash -c "systemctl restart ev3.service"

ssh rpi bash -c "cd sixers;git pull"
ssh rpi_root bash -c "systemctl daemon-reload"
ssh rpi_root bash -c "systemctl restart albert.service"
