#!/bin/bash

# Bắt đầu dịch vụ Suricata
echo "Starting Suricata service..."
sudo systemctl start suricata.service

# Chạy đồng thời hai tiến trình: suricata và cicflowmeter
echo "Starting Suricata and Cicflowmeter..."

# Tiến trình 1: Suricata
sudo suricata -c /etc/suricata/suricata.yaml -i ens33 &

# Tiến trình 2: Cicflowmeter (tuần tự)
cd /home/william/Desktop/cici_client/cicflowmeter-py
sudo cicflowmeter -i ens33 -c --dir /home/william/Desktop/cici_client/data/new &

# Chờ cả hai tiến trình hoàn thành
wait

echo "Suricata and Cicflowmeter started."
