import paramiko
import threading
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException


# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Tạo hoặc kết nối tới cơ sở dữ liệu và collection
db = client['cici_flow']
collection = db['monitor_host']

# Hàm thực thi lệnh từ xa qua SSH (tuần tự)
import paramiko
from paramiko.ssh_exception import SSHException

def execute_remote_command(remote_ip, username, password, command):
    """Thực thi lệnh trên máy từ xa và kiểm tra kết quả."""
    try:
        # Tạo một kết nối SSH tới máy từ xa
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, username=username, password=password)

        # Thực thi lệnh từ xa
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # Đợi lệnh hoàn tất và lấy mã thoát

        output = stdout.read().decode()   # Lấy đầu ra của lệnh
        error = stderr.read().decode()    # Lấy thông tin lỗi (nếu có)

        ssh.close()

        # Kiểm tra xem lệnh có thành công hay không
        if exit_status == 0:
            return output, None  # Nếu thành công, trả về output và None cho error
        else:
            return output, error  # Nếu thất bại, trả về cả output và error
    except SSHException as e:
        return None, f"SSHException: {str(e)}"
    except TimeoutError as e:
        return None, f"TimeoutError: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"



# Hàm để chạy tiến trình Suricata
def run_suricata(remote_ip, username, password):
    execute_remote_command(remote_ip, username, password, "sudo suricata -c /etc/suricata/suricata.yaml -i ens33")

# Hàm để chạy tiến trình Cicflowmeter
def run_cicflowmeter(remote_ip, username, password):
    # Chạy tuần tự hai lệnh
    execute_remote_command(remote_ip, username, password, "cd /home/william/Desktop/cici_client/cicflowmeter-py")
    execute_remote_command(remote_ip, username, password, "sudo cicflowmeter -i ens33 -c --dir /home/william/Desktop/cici_client/data/new")

def toggle_status(host_id):
    # Tìm host theo trường 'id' mà bạn định nghĩa
    host = collection.find_one({"id": host_id})

    if not host:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy host với id: {host_id}")
    
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
        message = f"Đã cập nhật thành công status của host có id: {host_id} từ {current_status} sang {new_status}"

        # Nếu chuyển trạng thái từ off sang on, bắt đầu theo dõi Suricata và Cicflowmeter song song
        if new_status == "on":
            message += f", bắt đầu theo dõi với Suricata và Cicflowmeter trên máy {remote_ip}..."
            
            output, error = execute_remote_command(remote_ip, username, password, "sudo systemctl start suricata.service")
            if error:
                raise HTTPException(status_code=500, detail=f"Lỗi khi khởi động Suricata: {error}")

            suricata_thread = threading.Thread(target=run_suricata, args=(remote_ip, username, password))
            cicflowmeter_thread = threading.Thread(target=run_cicflowmeter, args=(remote_ip, username, password))

            suricata_thread.start()
            cicflowmeter_thread.start()

            suricata_thread.join()
            cicflowmeter_thread.join()

        elif new_status == "off":
            message += f", dừng theo dõi với Suricata và Cicflowmeter trên máy {remote_ip}..."
            
            output, error = execute_remote_command(remote_ip, username, password, "sudo pkill -SIGINT suricata")
            if error:
                raise HTTPException(status_code=500, detail=f"Lỗi khi dừng Suricata: {error}")
            
            output, error = execute_remote_command(remote_ip, username, password, "sudo pkill -SIGINT cicflowmeter")
            if error:
                raise HTTPException(status_code=500, detail=f"Lỗi khi dừng Cicflowmeter: {error}")

            output, error = execute_remote_command(remote_ip, username, password, "sudo systemctl stop suricata.service")
            if error:
                raise HTTPException(status_code=500, detail=f"Lỗi khi dừng dịch vụ Suricata: {error}")
        
        return {"message": message}
    else:
        raise HTTPException(status_code=500, detail=f"Có lỗi xảy ra khi cập nhật status của host có id: {host_id}")





# #Ví dụ: Nhập id của host và chuyển đổi trạng thái
# host_id = int(input("Nhập id của host: "))  # Chuyển đổi input thành số nguyên
# toggle_status(host_id)

# # Đóng kết nối MongoDB
# client.close()
