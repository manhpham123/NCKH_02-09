#!/bin/bash

# Dừng tất cả các tiến trình liên quan đến Suricata
echo "Stopping all Suricata processes..."
suricata_pids=$(pgrep -f "suricata -c /etc/suricata/suricata.yaml -i ens33")

if [ -n "$suricata_pids" ]; then
    sudo kill $suricata_pids
    echo "Stopped Suricata processes: $suricata_pids"
else
    echo "No Suricata processes found."
fi

# Dừng tất cả các tiến trình liên quan đến Cicflowmeter
echo "Stopping all Cicflowmeter processes..."
cicflowmeter_pids=$(pgrep -f "/usr/bin/python3 /usr/local/bin/cicflowmeter -i ens33 -c --dir /home/william/Desktop/cici_client/data/new")

if [ -n "$cicflowmeter_pids" ]; then
    sudo kill $cicflowmeter_pids
    echo "Stopped Cicflowmeter processes: $cicflowmeter_pids"
else
    echo "No Cicflowmeter processes found."
fi

# Dừng dịch vụ Suricata sau khi tất cả các tiến trình đã bị dừng
echo "Stopping Suricata service..."
sudo systemctl stop suricata.service

if [ $? -eq 0 ]; then
    echo "Suricata service stopped successfully."
else
    echo "Failed to stop Suricata service."
fi

echo "All processes related to Suricata and Cicflowmeter have been stopped."
