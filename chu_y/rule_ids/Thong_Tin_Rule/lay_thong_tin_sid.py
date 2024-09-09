import re

def extract_sids(file_path):
    sids = []
    
    # Đọc file
    with open(file_path, 'r') as file:
        for line in file:
            # Sử dụng Regular Expression để tìm 'sid' trên mỗi dòng
            match = re.search(r'sid:(\d+);', line)
            if match:
                sids.append(match.group(1))
    
    return sids

# Đường dẫn đến file rule
#file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/bruce-force.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn
#file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/dos.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn
file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/Port_Scan.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn

# Gọi hàm và in ra các sid
sids = extract_sids(file_path)
for sid in sids:
    print(sid)

