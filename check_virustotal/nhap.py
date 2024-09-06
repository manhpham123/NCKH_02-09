# đây là code sau 70s để đọc 4 mã hash 1 lần và trả dữ liệu về db
#!/usr/bin/python3
import requests
from pymongo import MongoClient  # Thư viện để làm việc với MongoDB
import time  # Thư viện để tạo độ trễ

# Thay thế bằng API key của bạn
API_KEY = "d7f736ad869c2e43ff21bd3227b0b4e503b0ccaf87ef2545c219cb9991c47021"

class VirusTotal:
    def __init__(self):
        # Thiết lập tiêu đề cho các yêu cầu API
        self.headers = {"accept": "application/json", "x-apikey": API_KEY}
        self.url = "https://www.virustotal.com/api/v3/"

    def upload_hash(self, file_hash):
        # Tạo URL để tìm kiếm hash
        url = self.url + "search?query=" + file_hash
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            result = response.json()

            # Kiểm tra xem phản hồi có dữ liệu và lấy thông tin phân tích
            if len(result.get('data', [])) > 0:
                attributes = result['data'][0]['attributes']
                last_analysis_stats = attributes['last_analysis_stats']
                malicious = last_analysis_stats['malicious']
                total_engines = last_analysis_stats['harmless'] + last_analysis_stats['malicious'] + last_analysis_stats['suspicious'] + last_analysis_stats['undetected'] + last_analysis_stats['timeout']
                
                # Thu thập thông tin chi tiết về các công cụ phát hiện mã độc
                detections = []
                for engine_name, analysis in attributes['last_analysis_results'].items():
                    if analysis['category'] == 'malicious':
                        detections.append({
                            'engine_name': engine_name,
                            'result': analysis['result']
                        })
                
                # Lấy thông tin MD5, SHA1, SHA256 từ dữ liệu phản hồi
                md5 = attributes.get('md5', 'N/A')
                sha1 = attributes.get('sha1', 'N/A')
                sha256 = attributes.get('sha256', 'N/A')
                
                # Tạo dữ liệu trả về dưới dạng JSON
                result_data = {
                    "hash": {
                        "md5": md5,
                        "sha1": sha1,
                        "sha256": sha256
                    },
                    "score": f"{malicious}/{total_engines}",  # Điểm số: Số công cụ phát hiện mã độc / Tổng số công cụ
                    "malicious_count": malicious,
                    "total_engines": total_engines,
                    "detections": detections
                }
                return result_data
            else:
                return {
                    "hash": file_hash,
                    "message": "No data found"
                }
        
        except requests.exceptions.RequestException as e:
            return {
                "hash": file_hash,
                "error": str(e)
            }

def save_to_mongodb(data):
    # Kết nối tới MongoDB
    client = MongoClient('localhost', 27017)  # Kết nối tới MongoDB (chạy ở localhost và cổng 27017)
    db = client["hash_malware"]  # Tên cơ sở dữ liệu
    collection = db["hash_md5"]  # Tên collection

    # Lưu dữ liệu vào MongoDB
    collection.insert_one(data)
    print("Dữ liệu đã được lưu vào MongoDB.")

def check_hashes(hashes_to_check):
    virustotal = VirusTotal()
    
    # Kiểm tra từng nhóm 4 hash
    for i in range(0, len(hashes_to_check), 4):
        # Lấy nhóm 4 hash
        batch = hashes_to_check[i:i+4]
        
        for file_hash in batch:
            print(f"Checking hash: {file_hash}")
            result = virustotal.upload_hash(file_hash)
            print(result)
            if "error" not in result:  # Kiểm tra nếu không có lỗi
                save_to_mongodb(result)
        
        # Chờ 70 giây sau mỗi nhóm 4 hash
        if i + 4 < len(hashes_to_check):  # Kiểm tra nếu không phải nhóm cuối cùng
            print("Đang chờ 70 giây trước khi tiếp tục...")
            time.sleep(70)

def main():
    # Danh sách các hash để kiểm tra
    hashes_to_check = [
            # danh sách tất cả mã hash md5 ở đây, các mã đặt trong "" và cách nhau bằng dấu ,  . cứ 1 lần nó sẽ lấy 4 mã ra phân tích

    ]
    
    # Gọi hàm kiểm tra hash
    check_hashes(hashes_to_check)

if __name__ == "__main__":
    main()
