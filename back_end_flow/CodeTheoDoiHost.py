import paramiko
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Tạo hoặc kết nối tới cơ sở dữ liệu và collection
db = client['cici_flow']
collection = db['monitor_host']

# Hàm thực thi lệnh từ xa qua SSH và trả về kết quả
def execute_remote_command(remote_ip, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, username=username, password=password)

        # Thực thi lệnh từ xa
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        # Trả về kết quả hoặc lỗi (nếu có)
        if error:
            return {"success": False, "error": error}
        return {"success": True, "output": output}

    except Exception as e:
        return {"success": False, "error": str(e)}

# API để chuyển đổi trạng thái

def toggle_status(host_id):
    # Tìm host theo trường 'id' mà bạn định nghĩa
    host = collection.find_one({"id": host_id})

    if not host:
        raise HTTPException(status_code=400, detail=f"Không tìm thấy host với id: {host_id}")

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
        response = {
            "success": True,
            "message": f"Đã cập nhật thành công status của host có id: {host_id} từ {current_status} sang {new_status}"
        }

        # Nếu chuyển trạng thái từ off sang on, thực thi start.sh
        if new_status == "on":
            start_script = "/home/william/Documents/monitor_host/start.sh"
            cmd_result = execute_remote_command(remote_ip, username, password, f"bash {start_script}")
            response["start_script_result"] = cmd_result

        # Nếu chuyển trạng thái từ on sang off, thực thi stop.sh
        elif new_status == "off":
            stop_script = "/home/william/Documents/monitor_host/stop.sh"
            cmd_result = execute_remote_command(remote_ip, username, password, f"bash {stop_script}")
            response["stop_script_result"] = cmd_result

        # Trả về phản hồi thành công với mã trạng thái 200
        return response

    else:
        raise HTTPException(status_code=500, detail="Cập nhật trạng thái thất bại")
