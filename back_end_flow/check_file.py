import sqlite3
import json


import sqlite3
import json


def get_flow_file():
    # Đường dẫn đến file cơ sở dữ liệu SQLite
    sqlite_db_path = '/var/lib/evebox/events.sqlite'

    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Truy vấn để lấy trường `source` từ bảng `events` có chứa "event_type": "fileinfo"
    # và không chứa "filename" là "eve.json"
    query = """
    SELECT source FROM events
    WHERE json_extract(source, '$.event_type') = 'fileinfo'
    """


    # Thực thi truy vấn
    cursor.execute(query)

    # Lấy tất cả các hàng trả về
    rows = cursor.fetchall()
    
    # Danh sách để lưu các giá trị `source` có "event_type": "fileinfo"
    fileinfo_sources = []

    # Duyệt qua từng hàng và xử lý dữ liệu JSON
    for row in rows:
        try:
            # Chuyển đổi từ chuỗi JSON sang dict
            source_data = json.loads(row[0])
            
            # Kiểm tra thêm các điều kiện "http_content_type" và "fileinfo" khác None
            http_content_type = source_data.get("http", {}).get("http_content_type", "")
            fileinfo = source_data.get("fileinfo", None)
            
            if http_content_type == "application/octet-stream" and fileinfo is not None:
                # Trích xuất các trường cần thiết từ dữ liệu JSON
                result = {
                    "timestamp": source_data.get("timestamp"),
                    "src_ip": source_data.get("src_ip"),
                    "src_port": source_data.get("src_port"),
                    "dest_ip": source_data.get("dest_ip"),
                    "dest_port": source_data.get("dest_port"),
                    "protocol": source_data.get("proto"),
                    "filename": fileinfo.get("filename"),
                    "md5": fileinfo.get("md5")
                }
                # Thêm vào danh sách kết quả
                fileinfo_sources.append(result)
        except json.JSONDecodeError:
            # Nếu có lỗi khi chuyển đổi JSON, bỏ qua
            continue
    
    # Đóng kết nối
    conn.close()
    
    return fileinfo_sources
          
    # Đóng kết nối
    


# files = get_flow_file()
# # Hiển thị kết quả
# for source in files:
#     print(source)


