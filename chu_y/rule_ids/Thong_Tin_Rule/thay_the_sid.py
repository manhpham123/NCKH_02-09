import re

def replace_sids(file_path):
    # Đọc nội dung file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Khởi tạo biến đếm sid bắt đầu từ 1
    new_sid = 81
    
    # Danh sách để lưu các dòng đã thay đổi
    new_lines = []

    # Duyệt qua từng dòng và thay thế sid
    for line in lines:
        # Tìm kiếm 'sid' trong dòng và thay thế nó bằng 'sid' mới
        new_line = re.sub(r'sid:\d+;', f'sid:{new_sid};', line)
        new_lines.append(new_line)
        new_sid += 1  # Tăng sid lên 1 cho lần thay thế tiếp theo
    
    # Ghi lại nội dung mới vào file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f"SIDs trong file '{file_path}' đã được thay thế thành công.")

# Đường dẫn đến file rule
#file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/dos.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn
#file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/bruce-force.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn
file_path = '/home/frblam/NCKH_2024/NCKH_02-09/chu_y/rule_ids/Port_Scan.rules'  # Thay thế bằng đường dẫn thực tế đến file của bạn

# Gọi hàm để thay thế SIDs
replace_sids(file_path)

