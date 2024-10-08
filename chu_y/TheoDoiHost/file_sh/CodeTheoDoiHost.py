import paramiko
from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Tạo hoặc kết nối tới cơ sở dữ liệu và collection
db = client['cici_flow']
collection = db['monitor_host']

# Hàm thực thi lệnh từ xa qua SSH
def execute_remote_command(remote_ip, username, password, command):
    try:
        # Kết nối SSH tới máy từ xa
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, username=username, password=password)

        # Thực thi lệnh từ xa
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        # In kết quả và lỗi (nếu có)
        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

        ssh.close()
    except Exception as e:
        print(f"Lỗi khi thực thi lệnh từ xa: {e}")

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

        # Nếu chuyển trạng thái từ off sang on, bắt đầu thực thi file start.sh
        if new_status == "on":
            print(f"Bắt đầu theo dõi với Suricata trên máy {remote_ip}...")
            start_script = "/home/william/Documents/monitor_host/start.sh"
            execute_remote_command(remote_ip, username, password, f"bash {start_script}")
        
        # Nếu chuyển trạng thái từ on sang off, dừng theo dõi và thực thi file stop.sh
        elif new_status == "off":
            print(f"Dừng theo dõi với Suricata trên máy {remote_ip}...")
            stop_script = "/home/william/Documents/monitor_host/stop.sh"
            execute_remote_command(remote_ip, username, password, f"bash {stop_script}")

    else:
        print(f"Có lỗi xảy ra khi cập nhật status của host có id: {host_id}")

# Ví dụ: Nhập id của host và chuyển đổi trạng thái
host_id = int(input("Nhập id của host: "))  # Chuyển đổi input thành số nguyên
toggle_status(host_id)

# Đóng kết nối MongoDB
client.close()
