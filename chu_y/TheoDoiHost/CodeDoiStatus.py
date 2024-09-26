import paramiko
import threading
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Tạo hoặc kết nối tới cơ sở dữ liệu và collection
db = client['cici_flow']
collection = db['monitor_host']

# Hàm thực thi lệnh từ xa qua SSH (tuần tự)
def execute_remote_command(remote_ip, username, password, command):
    try:
        # Kết nối SSH tới máy từ xa
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, username=username, password=password)

        # Thực thi lệnh từ xa
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()  # Đợi lệnh hoàn tất

        output = stdout.read().decode()
        error = stderr.read().decode()

        # In kết quả và lỗi (nếu có)
        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

        ssh.close()
        return output.strip()  # Loại bỏ khoảng trắng thừa
    except Exception as e:
        print(f"Lỗi khi thực thi lệnh từ xa: {e}")
        return None

# Hàm để chạy tiến trình Suricata và lấy PID
def run_suricata(remote_ip, username, password):
    # Khởi động suricata và lấy PID
    execute_remote_command(remote_ip, username, password, "sudo systemctl start suricata.service")
    pid = execute_remote_command(remote_ip, username, password, "pgrep suricata")
    print(f"Suricata process started on {remote_ip} with PID: {pid}")
    return pid

# Hàm để chạy tiến trình Cicflowmeter và lấy PID
def run_cicflowmeter(remote_ip, username, password):
    # Chạy tuần tự hai lệnh và lấy PID của cicflowmeter
    execute_remote_command(remote_ip, username, password, "cd /home/william/Desktop/cici_client/cicflowmeter-py")
    execute_remote_command(remote_ip, username, password, "sudo cicflowmeter -i ens33 -c --dir /home/william/Desktop/cici_client/data/new")
    pid = execute_remote_command(remote_ip, username, password, "pgrep cicflowmeter")
    print(f"Cicflowmeter process started on {remote_ip} with PID: {pid}")
    return pid

def toggle_status(host_id):
    # Tìm host theo trường 'id' mà bạn định nghĩa
    host = collection.find_one({"id": host_id})

    if not host:
        print(f"Không tìm thấy host với id: {host_id}")
        return
    
    # Lấy thông tin máy từ xa từ cơ sở dữ liệu
    remote_ip = host.get("ip")
    username = host.get("username")
    password = host.get("password")

    # Lấy giá trị hiện tại của status
    current_status = host.get("status")

    # Chuyển đổi trạng thái
    new_status = "off" if current_status == "on" else "on"

    # Cập nhật status mới vào database
    result = collection.update_one(
        {"id": host_id},
        {"$set": {"status": new_status}}
    )

    if result.modified_count > 0:
        print(f"Đã cập nhật thành công status của host có id: {host_id} từ {current_status} sang {new_status}")

        # Nếu chuyển trạng thái từ off sang on, bắt đầu theo dõi Suricata và Cicflowmeter song song
        if new_status == "on":
            print(f"Bắt đầu theo dõi với Suricata và Cicflowmeter trên máy {remote_ip}...")
            
            # Khởi động Suricata và Cicflowmeter và lấy PID
            suricata_pid = run_suricata(remote_ip, username, password)
            cicflowmeter_pid = run_cicflowmeter(remote_ip, username, password)

            # In ra PID của cả hai tiến trình
            print(f"Suricata process with PID {suricata_pid} is running.")
            print(f"Cicflowmeter process with PID {cicflowmeter_pid} is running.")
        
        # Nếu chuyển trạng thái từ on sang off, dừng theo dõi Suricata và Cicflowmeter
        elif new_status == "off":
            print(f"Dừng theo dõi với Suricata và Cicflowmeter trên máy {remote_ip}...")

            # Lấy PID trước khi dừng và dừng cả hai tiến trình
            suricata_pid = execute_remote_command(remote_ip, username, password, "pgrep suricata")
            cicflowmeter_pid = execute_remote_command(remote_ip, username, password, "pgrep cicflowmeter")

            # Dừng Suricata và Cicflowmeter bằng tín hiệu Ctrl+C (SIGINT)
            execute_remote_command(remote_ip, username, password, "sudo pkill -SIGINT suricata")
            print(f"Suricata process with PID {suricata_pid} stopped on {remote_ip}")
            execute_remote_command(remote_ip, username, password, "sudo pkill -SIGINT cicflowmeter")
            print(f"Cicflowmeter process with PID {cicflowmeter_pid} stopped on {remote_ip}")
            
            # Sau khi cả hai tiến trình đã dừng, dừng dịch vụ Suricata
            execute_remote_command(remote_ip, username, password, "sudo systemctl stop suricata.service")
            print(f"Suricata service stopped on {remote_ip}")
    else:
        print(f"Có lỗi xảy ra khi cập nhật status của host có id: {host_id}")

# Ví dụ: Nhập id của host và chuyển đổi trạng thái
host_id = int(input("Nhập id của host: "))  # Chuyển đổi input thành số nguyên
toggle_status(host_id)

# Đóng kết nối MongoDB
client.close()
