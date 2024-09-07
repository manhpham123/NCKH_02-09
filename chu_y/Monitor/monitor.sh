#!/bin/bash
# 1. Khởi động Suricata
echo "Starting Monitor"
sudo systemctl start suricata.service

# 2. Theo dõi lưu lượng trên interface ens33
echo "Monitoring traffic on ens33..."
sudo suricata -c /etc/suricata/suricata.yaml -i ens33

# 3. Sau khi nhấn Ctrl+C, tắt theo dõi và dừng Suricata
echo "Stopping Monitor"
sudo systemctl stop suricata.service

# 4. Gửi log đến server qua Evebox agent
echo "Sending logs to server..."
evebox agent -c /etc/evebox/agent.yaml

