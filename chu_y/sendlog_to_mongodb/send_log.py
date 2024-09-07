import sqlite3
from pymongo import MongoClient
import datetime
import os

# Hàm chuyển đổi nanoseconds sang datetime
def nanoseconds_to_datetime(ns):
    seconds = ns / 1e9
    return datetime.datetime.fromtimestamp(seconds)

# Định nghĩa đường dẫn đến file lưu trữ thời gian của lần đọc cuối cùng
last_run_file = '/home/frblam/Documents/sendlog_to_mongodb/last_run_time.txt'

# Đọc thời gian của lần đọc cuối cùng
if os.path.exists(last_run_file):
    with open(last_run_file, 'r') as file:
        last_run_time_str = file.read().strip()
        if last_run_time_str:  # Kiểm tra nếu chuỗi không rỗng
            try:
                last_run_time = datetime.datetime.fromisoformat(last_run_time_str)
            except ValueError:
                # Nếu chuỗi không hợp lệ, sử dụng thời gian mặc định
                print(f"Invalid datetime format in {last_run_file}. Using default.")
                last_run_time = datetime.datetime(1970, 1, 1)  # Sử dụng thời gian mặc định hợp lệ
        else:
            # Nếu chuỗi rỗng, sử dụng thời gian mặc định
            last_run_time = datetime.datetime(1970, 1, 1)  # Sử dụng thời gian mặc định hợp lệ
else:
    # Nếu tệp không tồn tại, sử dụng thời gian mặc định
    last_run_time = datetime.datetime(1970, 1, 1)  # Sử dụng thời gian mặc định hợp lệ

# Kết nối đến cơ sở dữ liệu SQLite
sqlite_db_path = '/var/lib/evebox/events.sqlite'
try:
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
except sqlite3.OperationalError as e:
    print(f"Không thể mở tệp cơ sở dữ liệu: {e}")
    exit(1)

# Chuyển đổi thời gian của lần đọc cuối cùng sang nanoseconds
last_run_time_ns = last_run_time.timestamp() * 1e9

# Truy vấn để lấy các trường 'source' từ các bản ghi mới
query = """
SELECT source, timestamp
FROM events
WHERE timestamp > ?
"""
cursor.execute(query, (last_run_time_ns,))

# Kết nối đến MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['log_json']  # Thay 'log_json' bằng tên của cơ sở dữ liệu MongoDB
mongo_collection = mongo_db['full_log']  # Thay 'full_log' bằng tên của bảng trong MongoDB

# Chèn dữ liệu vào MongoDB
for row in cursor.fetchall():
    source_data = row[0]  # Lấy dữ liệu từ cột 'source'
    mongo_collection.insert_one({"source": source_data})

# Cập nhật thời gian của lần đọc cuối cùng
current_run_time = datetime.datetime.now().isoformat()
with open(last_run_file, 'w') as file:
    file.write(current_run_time)

# Đóng kết nối
cursor.close()
conn.close()
mongo_client.close()

print("Dữ liệu mới đã được chuyển thành công!")

