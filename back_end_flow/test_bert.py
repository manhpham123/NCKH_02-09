import sys
import os
import time
from logging import getLogger

import numpy as np
from scapy.all import Ether, CookedLinux

import ailia
import torch

# import original modules
# sys.path.append("../../util")
# from arg_utils import get_base_parser, update_parser
# from model_utils import check_and_download_models
# from math_utils import softmax
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pymongo import MongoClient
from scapy.all import sniff, IP, TCP, raw
client = MongoClient("mongodb://localhost:27017/")
db = client["cici_flow"]
ip = "192.168.189.133"
intf_str = "ens33"
collection_packets = db[f"packet_{ip}_{intf_str}"]

def read_raw_payload(collection_name, flow_id):
    cursor = collection_name.find_one({"flow_id": flow_id})
    if cursor is None:
        return {}
    # Chuyển đổi dữ liệu từ cursor thành danh sách các từ điển (dict)
    # raw_payload_flow = []
    # for doc in cursor:
    #     raw_payload_flow.append(doc)
    return cursor

def read_all_payload (collection_name):
    cursor = collection_name.find()
    raw_payload = []
    for doc in cursor: 
        raw_payload.append(doc)
    return raw_payload
def read_packets_from_file(file_path):
    packets = []
    with open(file_path, 'r') as file:
        for line in file:
            # Xóa ký tự xuống dòng
            packet_hex = line.strip()
            packets.append(packet_hex)
    return packets

def use_packets(packets):
    for packet_hex in packets:
        # Xử lý từng gói tin hex
        print(f"Processing hex: {packet_hex}")
        # Bạn có thể thêm mã xử lý gói tin ở đây

# Đọc các gói tin từ file


# Sử dụng các gói tin đã đọc


LABELS = [
    "DoS Slowloris",
    "Normal",
    "Port Scan",
    "SSH Patator",
    "Web Attack - SQL Injection",
    "Web Attack - XSS"
]

def softmax(x, axis=None):
    max = np.max(x, axis=axis, keepdims=True)
    e_x = np.exp(x - max)
    sum = np.sum(e_x, axis=axis, keepdims=True)
    f_x = e_x / sum
    return f_x


def preprocess(packet_hex):
    packet_bytes = bytes.fromhex(packet_hex)
    packet = Ether(packet_bytes)
    
    # Kiểm tra và xử lý loại frame
    if packet.firstlayer().name != "Ethernet":
        packet = CookedLinux(packet_bytes)
        if packet.firstlayer().name != "cooked linux":
            raise ValueError(
                f"{packet.firstlayer().name} frame not implemented. Ethernet and Cooked Linux are only supported."
            )

    # Kiểm tra xem gói tin có lớp "IP" và "TCP" không
    if "IP" not in packet or "TCP" not in packet:
        raise ValueError("Only TCP/IP packets are supported.")

    forward_packets = 0
    backward_packets = 0
    bytes_transfered = len(packet_bytes)

    # Trích xuất thông tin cần thiết để tạo feature.
    src_ip = packet["IP"].src
    dst_ip = packet["IP"].dst
    ip_length = len(packet["IP"])
    ip_ttl = packet["IP"].ttl
    ip_tos = packet["IP"].tos
    src_port = packet["TCP"].sport
    dst_port = packet["TCP"].dport
    tcp_data_offset = packet["TCP"].dataofs
    tcp_flags = packet["TCP"].flags

    # Xử lý nội dung payload và tạo chuỗi feature.
    if "IP" in packet and "TCP" in packet:
        payload_bytes = bytes(packet["TCP"].payload)  # Sử dụng payload của TCP nếu có
    else:
        payload_bytes = bytes(packet["IP"].payload)  # Sử dụng payload của IP nếu không có TCP
    
    payload_length = len(payload_bytes)
    payload_decimal = [str(byte) for byte in payload_bytes]

    final_data = [
        forward_packets,
        backward_packets,
        bytes_transfered,
        -1,
        src_port,
        dst_port,
        ip_length,
        payload_length,
        ip_ttl,
        ip_tos,
        tcp_data_offset,
        int(tcp_flags),
        -1,
    ] + payload_decimal

    if len(payload_decimal) > 0:
        final_data = " ".join(str(s) for s in final_data)
        return final_data  
    else:
        return ""
packets_brief = {}
forward_packets = {}
backward_packets = {}
protocols = []
protocol_counts = {}

def processing_packet_conversion(packet_hex):
    # Chuyển đổi chuỗi hex thành dạng byte
    packet_bytes = bytes.fromhex(packet_hex)
    
    # Tạo đối tượng gói tin từ byte (Ethernet hoặc CookedLinux)
    packet = Ether(packet_bytes)
    if packet.firstlayer().name != "Ethernet":
        packet = CookedLinux(packet_bytes)
        if packet.firstlayer().name != "cooked linux":
            raise ValueError(
                f"{packet.firstlayer().name} frame not implemented. Ethernet and Cooked Linux are only supported."
            )

    # Tạo một bản sao của gói tin để xử lý mà không làm thay đổi gói tin gốc
    packet_2 = packet.copy()

    while packet_2:
        # Trích xuất và đếm các lớp giao thức trong gói tin.
        layer = packet_2[0]
        if layer.name not in protocol_counts:
            protocol_counts[layer.name] = 1  # Bắt đầu đếm từ 1
        else:
            protocol_counts[layer.name] += 1
        protocols.append(layer.name)

        # Thoát khỏi vòng lặp nếu không còn lớp payload nào
        if not layer.payload:
            break
        packet_2 = layer.payload

    # Kiểm tra xem gói tin có các lớp IP và TCP không
    if IP not in packet or TCP not in packet:
        raise ValueError("Only TCP/IP packets are supported.")

    # Trích xuất thông tin cần thiết cho việc tạo feature.
    src_ip = packet["IP"].src
    dst_ip = packet["IP"].dst
    src_port = packet["TCP"].sport
    dst_port = packet["TCP"].dport
    ip_length = len(packet["IP"])
    ip_ttl = packet["IP"].ttl
    ip_tos = packet["IP"].tos
    tcp_data_offset = packet["TCP"].dataofs
    tcp_flags = packet["TCP"].flags

    # Xử lý nội dung payload và tạo chuỗi feature.
    payload_bytes = bytes(packet["TCP"].payload)  # Lấy payload từ lớp TCP
    payload_length = len(payload_bytes)
    # Chuyển payload thành chuỗi ký tự
    payload_content = payload_bytes.decode('utf-8', 'replace')
    # Chuyển đổi payload thành chuỗi số thập phân
    payload_decimal = ' '.join(str(byte) for byte in payload_bytes)
    
    # Tạo chuỗi dữ liệu đặc trưng
    final_data = "0" + " " + "0" + " " + "195" + " " + "-1" + " " + \
                 str(src_port) + " " + str(dst_port) + " " + str(ip_length) + " " + \
                 str(payload_length) + " " + str(ip_ttl) + " " + str(ip_tos) + " " + \
                 str(tcp_data_offset) + " " + str(int(tcp_flags)) + " " + "-1" + " " + payload_decimal
    
    return final_data


import time

def predict(models, processed_packet):
    # Bắt đầu đếm thời gian
    start_time = time.time()

    # Tiền xử lý packet_hex
    final_format = processed_packet

    # Khởi tạo tokenizer
    tokenizer = models["tokenizer"]
    
    # Mã hóa dữ liệu đầu vào
    model_inputs = tokenizer(final_format[:1024], return_tensors="pt", truncation=True, max_length=512)  # Sử dụng "pt" cho PyTorch
    input_ids = model_inputs["input_ids"]
    attention_mask = model_inputs["attention_mask"]

    # Khởi tạo mô hình từ transformers
    model = models["model"]

    # Thực hiện dự đoán
    with torch.no_grad():
        output = model(input_ids, attention_mask=attention_mask)

    # Lấy giá trị logits từ output
    logits = output.logits

    # Tính xác suất với softmax
    scores = softmax(logits[0].numpy())
    # Sắp xếp các nhãn theo thứ tự xác suất giảm dần
    idx = np.argsort(-scores)
    labels = np.array(LABELS)[idx]
    scores = scores[idx]

    # Kết thúc đếm thời gian
    prediction_time = time.time() - start_time
    print(f"Thời gian dự đoán: {prediction_time:.4f} giây")

    return (labels, scores, prediction_time)




attack_label = {}
def recognize_from_packet(models, packet_hex, flow_id):
    #packet_hex = args.hex
    # if packet_hex:
    #     args.input[0] = packet_hex

    # # input audio loop
    # for packet_path in args.input:
    #     # prepare input data
    #     if os.path.isfile(packet_path):
    #         logger.info(packet_path)
    #         with open(packet_path, "r") as f:
    #             packet_hex = f.read()
    output = predict(models, packet_hex)
        # # inference
        # logger.info("Start inference...")
        # if args.benchmark:
        #     logger.info("BENCHMARK mode")
        #     total_time_estimation = 0
        #     for i in range(args.benchmark_count):
        #         start = int(round(time.time() * 1000))
        #         output = predict(models, packet_hex)
        #         end = int(round(time.time() * 1000))
        #         estimation_time = end - start

        #         # Logging
        #         logger.info(f"\tailia processing estimation time {estimation_time} ms")
        #         if i != 0:
        #             total_time_estimation = total_time_estimation + estimation_time

        #     logger.info(
        #         f"\taverage time estimation {total_time_estimation / (args.benchmark_count - 1)} ms"
        #     )
        # else:
        #     output = predict(models, packet_hex)

    
    labels, socres = output
    if flow_id not in attack_label:
        attack_label[flow_id] = {}
    
    top_k = 3
    for label, score in list(zip(labels, socres))[:top_k]:
        print(f"{label} : {score*100:.3f}")
        if label in attack_label[flow_id]:
            if score*100 > 70:
                attack_label[flow_id][label] += 1
                #print("hello: ", attack_label[flow_id][label])          
        else:
            if score*100 > 70:
                #print(score*100)
                attack_label[flow_id][label] = 1
            else :
                attack_label[flow_id][label] = 0
            
    #print(attack_label[flow_id])
    return labels, socres
    
    #print("Script finished successfully.")
    
MODEL_DIR = "/home/frblam/NCKH_2024/NCKH_02-09/New_bert"
TOKENIZER_DIR = "/home/frblam/NCKH_2024/NCKH_02-09/New_bert"

def load_model_and_tokenizer(model_dir, tokenizer_dir):
    # Kiểm tra xem model và tokenizer đã tồn tại chưa
    if not os.path.exists(model_dir) or not os.path.exists(tokenizer_dir):
        print("Mô hình hoặc tokenizer chưa tồn tại, đang tải xuống...")

        # Tải và lưu tokenizer
        tokenizer = AutoTokenizer.from_pretrained("rdpahalavan/bert-network-packet-flow-header-payload")
        tokenizer.save_pretrained(tokenizer_dir)

        # Tải và lưu model
        model = AutoModelForSequenceClassification.from_pretrained("rdpahalavan/bert-network-packet-flow-header-payload")
        model.save_pretrained(model_dir)

        print("Mô hình và tokenizer đã được tải và lưu cục bộ.")
    else:
        print("Mô hình và tokenizer đã tồn tại, tải từ thư mục cục bộ.")

    # Load model và tokenizer từ thư mục cục bộ
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    return model, tokenizer

def print_result(labels, socres):
    attack_lable = {}
    top_k = 3
    for label, score in list(zip(labels, socres))[:top_k]:
        print(f"{label} : {score*100:.3f}")
        if label in attack_lable:
            if score*100 > 50:
                attack_lable[label] += 1
        else: 
            attack_lable[label] = 0
            
    return attack_lable
def bert_pred(flow_id, collection_name):
    attack_label = {}
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3
    for packet in packets:
        labels, scores = recognize_from_packet(models, packet, flow_payload["flow_id"])
        for label, score in list(zip(labels, scores))[:top_k]:
        #print(f"{label} : {score*100:.3f}")
            if label != "Normal":
                if label in attack_label :
                    if score*100 > 50:
                        attack_label[label] += 1
                        #print("hello: ", attack_label[flow_id][label])          
                else:
                    if score*100 > 50:
                        #print(score*100)
                        attack_label[label]= 1
                    else :
                        attack_label[label]= 0
    return attack_label

def bert_pred_stats(flow_id, collection_name, attack_threshold=50, score_threshold=50):
    """
    Dự đoán nhãn của các packets trong một flow và tính số lượng packets, tổng điểm có trọng số, 
    và trung bình % dự đoán cho mỗi nhãn tấn công. 
    Nếu số lượng packets có nhãn "Normal" chiếm hơn 95% tổng số packets, thì kết quả của flow là "Normal". 
    Chỉ tính điểm cho các nhãn tấn công nếu score của nhãn đó vượt qua ngưỡng `score_threshold`.
    """
    weight_table = {
        "Analysis": 1, "Backdoor": 5, "Bot": 4, "DDoS": 5, "DoS": 4,
        "DoS GoldenEye": 4, "DoS Hulk": 4, "DoS SlowHTTPTest": 4, "DoS Slowloris": 4,
        "Exploits": 5, "FTP Patator": 2, "Fuzzers": 2, "Generic": 1, "Heartbleed": 2,
        "Infiltration": 5, "Port Scan": 3, "Reconnaissance": 3, "SSH Patator": 2,
        "Shellcode": 5, "Web Attack - Brute Force": 3, "Web Attack - SQL Injection": 4,
        "Web Attack - XSS": 3, "Worms": 5
    }

    attack_stats = {}
    normal_count = 0
    total_packets = 0
    labels_above_threshold = []
    normal = {'label': "Normal", 'count': 0, 'total_score': 0.0, 'average_score': 0.0, 'packet_ratio': '0/0'}
    
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {"tokenizer": tokenizer, "model": model}
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3
    total_time = 0

    # Duyệt qua từng packet để dự đoán nhãn
    for packet in packets:
        packet = preprocess(packet)
        total_packets += 1
        try:
            output = predict(models, packet)
            labels, scores, pk_time = output
            total_time += pk_time
        except ValueError:
            continue

        for label, score in zip(labels[:top_k], scores[:top_k]):
            
            print(label, score)
            if score * 100 < score_threshold:
                continue

            if label == "Normal":
                normal_count += 1
                normal['count'] += 1
                normal['total_score'] += score * 100
            else:
                if label not in attack_stats:
                    attack_stats[label] = {'count': 0, 'total_score': 0.0, 'average_percentage_score': 0.0, 'packet_ratio': '0/0'}
                attack_stats[label]['count'] += 1
                attack_stats[label]['total_score'] += score * 100

    # Tính toán điểm trung bình và tỉ lệ phần trăm packet cho Normal
    if normal['count'] > 0:
        normal['average_percentage_score'] = normal['total_score'] / normal['count']
        normal['packet_ratio'] = f"{normal['count']}/{total_packets}"
        normal['percentage_packets'] = (normal['count'] / total_packets) * 100

    # Nếu số lượng packets Normal > 99%, trả về Normal với cùng định dạng với các nhãn tấn công
    if normal_count / total_packets > 0.99:
        return [normal], total_time, total_packets

    # Tính toán trung bình % dự đoán cho mỗi nhãn tấn công và kiểm tra ngưỡng tấn công
    for label, stats in attack_stats.items():
        stats['average_score'] = stats['total_score'] / stats['count']
        stats['packet_ratio'] = f"{stats['count']}/{total_packets}"
        stats['percentage_packets'] = (stats['count'] / total_packets) * 100
        
        # Kiểm tra nếu nhãn có điểm trung bình vượt qua ngưỡng
        if stats['average_score'] >= attack_threshold:
            labels_above_threshold.append({
                'label': label,
                'average_percentage_score': stats['average_score'],
                'packet_ratio': stats['packet_ratio'],
            })

    # Nếu không có nhãn tấn công nào vượt ngưỡng, trả về Normal với định dạng đồng nhất
    if not labels_above_threshold:
        return [normal], total_time, total_packets

    # Trả về danh sách các nhãn tấn công có định dạng đồng nhất với nhãn Normal
    return labels_above_threshold, total_time, total_packets








def bert_pred_pt(flow_id, collection_name):
    attack_label = {}  # Tạo dictionary để lưu tổng số điểm và số lần xuất hiện của mỗi nhãn
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3
    total_packet = 0

    # Duyệt qua từng packet để dự đoán nhãn
    for packet in packets:
        packet = preprocess(packet)
        try:
            output = predict(models, packet)
            labels, scores = output
        except ValueError as e:
            # Bỏ qua packet không phải là TCP/IP
            print(f"Packet không phải là TCP/IP cho flow_id {flow_id}: {str(e)}")
            continue
        for label, score in list(zip(labels, scores))[:top_k]:
            total_packet += 1
            # Nếu nhãn đã có trong attack_label, cập nhật tổng điểm và số lần xuất hiện
            #if label != "Normal":
            
            if label in attack_label:
                attack_label[label]["total_score"] += score * 100  # Cộng tổng điểm
                attack_label[label]["count"] += 1
                
            else:
                # Nếu nhãn chưa có trong attack_label, khởi tạo
                attack_label[label] = {"total_score": score * 100, "count": 1}

    # Tính toán trung bình % dự đoán của mỗi nhãn
    average_attack_label = {}
    for label, data in attack_label.items():
        average_attack_label[label] = data["total_score"] / total_packet  # Tính trung bình

    return average_attack_label  # Trả về kết quả là dictionary chứa trung bình % dự đoán của mỗi nhãn

def bert_pred_max(flow_id, collection_name):
    attack_label = {}  # Dictionary để lưu tổng điểm của mỗi nhãn
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3

    # Duyệt qua từng packet để dự đoán nhãn
    for packet in packets:
        try:
            labels, scores = recognize_from_packet(models, packet, flow_payload["flow_id"])
        except ValueError as e:
            # Bỏ qua packet không phải là TCP/IP
            print(f"Packet không phải là TCP/IP cho flow_id {flow_id}: {str(e)}")
            continue
        
        # Cập nhật tổng điểm cho mỗi nhãn
        for label, score in list(zip(labels, scores))[:top_k]:
            # Nếu nhãn đã có trong attack_label, cộng dồn tổng điểm
            if label in attack_label:
                attack_label[label] += score * 100  # Cộng tổng điểm
            else:
                # Nếu nhãn chưa có trong attack_label, khởi tạo
                attack_label[label] = score * 100

    # Tìm nhãn có tổng xác suất cao nhất
    if not attack_label:
        return None  # Không có nhãn nào được dự đoán

    # Lấy nhãn có tổng điểm cao nhất
    highest_label = max(attack_label, key=attack_label.get)

    return highest_label, attack_label[highest_label]  # Trả về nhãn có tổng điểm cao nhất

def bert_pred_hybrid(flow_id, collection_name, attack_threshold=20):
    """
    Xác định nhãn của một flow dựa trên tỉ lệ dự đoán nhãn của các packets,
    đồng thời giảm ảnh hưởng của nhãn "Normal" bằng cách tập trung vào các nhãn tấn công.

    Args:
    - flow_id (str): ID của flow cần dự đoán.
    - collection_name (str): Tên của bộ sưu tập chứa dữ liệu flow.
    - attack_threshold (int): Ngưỡng tỉ lệ để quyết định nhãn tấn công (mặc định là 20%).

    Returns:
    - str: Nhãn của flow hoặc "Normal" nếu không đạt ngưỡng tấn công.
    """
    attack_label = {}  # Dictionary để lưu tổng điểm của mỗi nhãn không phải "Normal"
    normal_count = 0   # Biến đếm số lượng packets được dự đoán là "Normal"
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3

    # Duyệt qua từng packet để dự đoán nhãn
    for packet in packets:
        try:
            labels, scores = recognize_from_packet(models, packet, flow_payload["flow_id"])
        except ValueError as e:
            # Bỏ qua packet không phải là TCP/IP
            print(f"Packet không phải là TCP/IP cho flow_id {flow_id}: {str(e)}")
            continue
        
        # Cập nhật tổng điểm cho mỗi nhãn
        for label, score in list(zip(labels, scores))[:top_k]:
            print(f"{label} : {score*100:.3f}")
            if label == "Normal":
                normal_count += 1  # Tăng số lượng packets "Normal"
            else:
                # Nếu là nhãn tấn công, cộng dồn tổng điểm cho nhãn đó
                if label in attack_label:
                    attack_label[label] += score * 100  # Cộng tổng điểm
                else:
                    attack_label[label] = score * 100

    # Tổng số packets đã xử lý
    total_packets = len(packets)

    # Nếu không có nhãn tấn công nào hoặc tất cả là "Normal"
    if not attack_label or total_packets == normal_count:
        return "Normal"  # Tất cả packets đều "Normal"

    # Tính tỉ lệ các nhãn tấn công
    attack_ratios = {label: (score / (total_packets * 100)) * 100 for label, score in attack_label.items()}

    # Chọn nhãn tấn công có tỉ lệ cao nhất nếu vượt qua ngưỡng, nếu không thì trả về "Normal"
    for label, ratio in attack_ratios.items():
        if ratio >= attack_threshold:
            return label  # Nhãn tấn công có tỉ lệ vượt ngưỡng

    return "Normal"  # Trả về "Normal" nếu không có nhãn tấn công nào vượt ngưỡng

def bert_pred_hybrid_improved(flow_id, collection_name, attack_threshold=20, window_size=5):
    """
    Xác định nhãn của một flow dựa trên tỉ lệ dự đoán nhãn của các packets
    và sử dụng cửa sổ trượt để tăng cường độ chính xác phát hiện tấn công.

    Args:
    - flow_id (str): ID của flow cần dự đoán.
    - collection_name (str): Tên của bộ sưu tập chứa dữ liệu flow.
    - attack_threshold (int): Ngưỡng tỉ lệ để quyết định nhãn tấn công (mặc định là 20%).
    - window_size (int): Kích thước của cửa sổ trượt để phân tích các packet.

    Returns:
    - str: Nhãn của flow hoặc "Normal" nếu không đạt ngưỡng tấn công.
    """
    attack_label = {}  # Dictionary để lưu tổng điểm của mỗi nhãn không phải "Normal"
    normal_count = 0   # Biến đếm số lượng packets được dự đoán là "Normal"
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)
    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    flow_payload = read_raw_payload(collection_name, flow_id=flow_id)
    packets = flow_payload["raw_payload"]
    top_k = 3

    # Duyệt qua từng packet để dự đoán nhãn theo cửa sổ trượt
    for i in range(0, len(packets), window_size):
        window_packets = packets[i:i+window_size]  # Lấy các packet trong cửa sổ
        for packet in window_packets:
            try:
                labels, scores = recognize_from_packet(models, packet, flow_payload["flow_id"])
            except ValueError:
                # Bỏ qua packet không phải là TCP/IP
                continue
            
            # Cập nhật tổng điểm cho mỗi nhãn
            for label, score in list(zip(labels, scores))[:top_k]:
                if label == "Normal":
                    normal_count += 1  # Tăng số lượng packets "Normal"
                else:
                    # Nếu là nhãn tấn công, cộng dồn tổng điểm cho nhãn đó
                    attack_label[label] = attack_label.get(label, 0) + score * 100

    # Tổng số packets đã xử lý
    total_packets = len(packets)

    # Nếu không có nhãn tấn công nào hoặc tất cả là "Normal"
    if not attack_label or total_packets == normal_count:
        return "Normal"  # Tất cả packets đều "Normal"

    # Tính tỉ lệ các nhãn tấn công và quyết định nhãn cuối cùng
    for label, score in attack_label.items():
        ratio = (score / (total_packets * 100)) * 100  # Tỉ lệ nhãn tấn công
        if ratio >= attack_threshold:
            return label  # Nhãn tấn công có tỉ lệ vượt ngưỡng

    return "Normal"  # Trả về "Normal" nếu không có nhãn tấn công nào vượt ngưỡng



def main():
    #model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)

    # models = {
    #     "tokenizer": tokenizer,
    #     "model": model,
    # }
    print("hello")
    count = 0
    
    packets = read_packets_from_file('packets.txt')
    # flow = read_raw_payload(collection_packets, "fl00003")
    # packets = flow["raw_payload"]
    
    #flows = read_all_payload(collection_packets)
    
    
    
    # for flow in flows:
    #     fl_id = flow["flow_id"]
    #     stt = int(fl_id[2:])
    #     if stt > 561:
    #         packets = flow["raw_payload"]
    #         for packet in packets:
    #             print(fl_id)
    #             lables, scores = recognize_from_packet(models, packet, fl_id)
            
    #         print(f"flow_id : {fl_id}" ,attack_label[fl_id])
        
    #print(bert_pred_stats("fl00003", collection_packets))
    
    # for packet_hex in packets:
    #     count += 1
    #     if count == 800:
    #         break
    #recognize_from_packet(models, packet_hex)
    print(bert_pred_stats("fl05988", collection_packets))   
main()