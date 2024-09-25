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
    SELECT ROWID ,source FROM events
    WHERE json_extract(source, '$.event_type') = 'fileinfo'
    ORDER BY json_extract(source, '$.timestamp') DESC
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
            source_data = json.loads(row[1])
            id = row[0]
            
            # Kiểm tra thêm các điều kiện "http_content_type" và "fileinfo" khác None
            http_content_type = source_data.get("http", {}).get("http_content_type", "")
            fileinfo = source_data.get("fileinfo", None)
            
            if http_content_type == "application/octet-stream" and fileinfo is not None:
                # Trích xuất các trường cần thiết từ dữ liệu JSON
                result = {
                    "_id": id,
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


import sqlite3
import json

# Hàm chuyển đổi dữ liệu từ query thành định dạng JSON mong muốn
def transform_data(events):
    transformed_data = []

    for event in events:
        source_data = json.loads(event[1])  # Cột 'source' chứa JSON trong cơ sở dữ liệu
        row_id = event[0]
        transformed_event = {
            "_id": row_id,
            "timestamp": source_data.get("timestamp"),
            "src_ip": source_data.get("src_ip"),
            "src_port": source_data.get("src_port"),
            "dest_ip": source_data.get("dest_ip"),
            "dest_port": source_data.get("dest_port"),
            "protocol": source_data.get("proto"),
            "signature": source_data.get("alert", {}).get("signature"),
            "signature_id": source_data.get("alert", {}).get("signature_id"),
            "severity": source_data.get("alert", {}).get("severity")
            #"flow_id": f"fl{str(source_data.get('flow_id'))[-5:]}"  # Giả định flow_id
        }
        transformed_data.append(transformed_event)

    return transformed_data

# Hàm đọc dữ liệu từ SQLite và trả về kết quả sau khi xử lý
def read_events_from_db(db_path):
    # Kết nối tới cơ sở dữ liệu
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Truy vấn dữ liệu
    query = """ SELECT ROWID ,source FROM events 
    WHERE json_extract(source, '$.event_type') = 'alert'
    ORDER BY json_extract(source, '$.timestamp') DESC """
    cursor.execute(query)

    # Lấy tất cả các bản ghi trả về từ truy vấn
    events = cursor.fetchall()

    # Đóng kết nối
    conn.close()

    # Chuyển đổi dữ liệu
    return transform_data(events)

# Đường dẫn tới cơ sở dữ liệu SQLite


def get_rule_alert():
    db_path = '/var/lib/evebox/events.sqlite'
    result = read_events_from_db(db_path)

# In kết quả ra dưới dạng JSON đẹp (pretty-printed JSON)
    #return json.dumps(result)
    return result




print(get_rule_alert())
# files = get_flow_file()
# # Hiển thị kết quả
# for source in files:
#     print(source)


