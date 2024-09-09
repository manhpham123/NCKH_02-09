import subprocess
import time

# Danh sách các kiểu quét tối ưu để tạo ra nhiều lưu lượng nhất
optimized_scan_types = {
    "Intensive SYN Scan": "-sS -p- ",
    "Intensive TCP Connect Scan": "-sT -p- ",
    "Intensive UDP Scan": "-sU -p- --max-retries 5",
    "Aggressive Scan": "-A -",
    "Service Version Detection Scan": "-sV --version-intensity 9",
    "OS Detection Scan": "-O --osscan-guess",
    "All TCP Ports Scan": "-p- -sS ",
    "All Protocols Scan": "-sO",
    "Intensive XMAS Scan": "-sX -p- "
}

def run_nmap_scan(scan_type, options, target_ip, output_file):
    """
    Hàm để chạy một loại quét nmap tối ưu và ghi kết quả vào tệp.
    """
    command = f"nmap {options} {target_ip} -oN {output_file}"
    try:
        # Sử dụng subprocess để chạy câu lệnh nmap
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{scan_type} completed. Results saved in {output_file}.")
    except subprocess.CalledProcessError as e:
        # Xử lý lỗi nếu có
        print(f"Error running {scan_type}: {e.stderr.decode()}")

def run_all_optimized_scans(target_ip, repeat_times=1, delay_between_scans=5):
    """
    Hàm để chạy tất cả các kiểu quét tối ưu nhiều lần.
    """
    for _ in range(repeat_times):
        for scan_type, options in optimized_scan_types.items():
            # Đặt tên file kết quả
            output_file = f"nmap_{scan_type.replace(' ', '_').lower()}_scan_results.txt"
            # Chạy quét nmap với các tùy chọn tối ưu
            run_nmap_scan(scan_type, options, target_ip, output_file)
            # Thời gian chờ giữa các lần quét để tránh quá tải hệ thống
            time.sleep(delay_between_scans)

if __name__ == "__main__":
    # Địa chỉ IP mục tiêu (thay đổi theo nhu cầu của bạn)
    target_ip = "192.168.10.10"
    
    # Số lần lặp lại cho mỗi kiểu quét
    repeat_times = 30  # Ví dụ: chạy 2 lần
    
    # Khoảng thời gian chờ giữa các lần quét (giây)
    delay_between_scans = 10
    
    # Chạy tất cả các kiểu quét tối ưu
    run_all_optimized_scans(target_ip, repeat_times, delay_between_scans)
