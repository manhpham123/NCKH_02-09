#!/bin/bash

# Bắt đầu dịch vụ Suricata
echo "Starting Suricata service..."
sudo systemctl start suricata.service

# Chạy đồng thời hai tiến trình: suricata và cicflowmeter
echo "Starting Suricata and Cicflowmeter..."

# Tiến trình 1: Suricata
nohup sudo suricata -c /etc/suricata/suricata.yaml -i ens33 > /dev/null 2>&1 &

# Tiến trình 2: Cicflowmeter (tuần tự)
cd /home/william/Desktop/cici_client/cicflowmeter-py
nohup sudo cicflowmeter -i ens33 -c --dir /home/william/Desktop/cici_client/data/new > /dev/null 2>&1 &

# In ra thông báo hoàn thành
echo "Suricata and Cicflowmeter started and running in background."

# Thoát khỏi script
exit 0
