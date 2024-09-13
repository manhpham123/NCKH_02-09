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
intf_str = "ens36"
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
    "Analysis",
    "Backdoor",
    "Bot",
    "DDoS",
    "DoS",
    "DoS GoldenEye",
    "DoS Hulk",
    "DoS SlowHTTPTest",
    "DoS Slowloris",
    "Exploits",
    "FTP Patator",
    "Fuzzers",
    "Generic",
    "Heartbleed",
    "Infiltration",
    "Normal",
    "Port Scan",
    "Reconnaissance",
    "SSH Patator",
    "Shellcode",
    "Web Attack - Brute Force",
    "Web Attack - SQL Injection",
    "Web Attack - XSS",
    "Worms",
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
    if packet.firstlayer().name != "Ethernet":
        packet = CookedLinux(packet_bytes)
        if packet.firstlayer().name != "cooked linux":
            raise ValueError(
                f"{packet.firstlayer().name} frame not implemented. Ethernet and Cooked Linux are only supported."
            )

    if "IP" not in packet or "TCP" not in packet:
        raise ValueError("Only TCP/IP packets are supported.")

    forward_packets = 0
    backward_packets = 0
    bytes_transfered = len(packet_bytes)

    # Extract relevant information for feature creation.
    src_ip = packet["IP"].src
    dst_ip = packet["IP"].dst
    ip_length = len(packet["IP"])
    ip_ttl = packet["IP"].ttl
    ip_tos = packet["IP"].tos
    src_port = packet["TCP"].sport
    dst_port = packet["TCP"].dport
    tcp_data_offset = packet["TCP"].dataofs
    tcp_flags = packet["TCP"].flags

    # Process payload content and create a feature string.
    #payload_bytes = bytes(packet["IP"].payload if args.ip else packet["TCP"].payload)
    payload_bytes = bytes(packet["TCP"].payload)
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

    final_data = " ".join(str(s) for s in final_data)
    return final_data

def predict(models, packet_hex):
    # Tiền xử lý packet_hex
    final_format = preprocess(packet_hex)

    # Khởi tạo tokenizer
    tokenizer = models["tokenizer"]
    # Mã hóa dữ liệu đầu vào
    model_inputs = tokenizer(final_format[:1024], return_tensors="pt")  # Sử dụng "pt" cho PyTorch
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

    return (labels, scores)



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
    
MODEL_DIR = "/home/frblam/NCKH_2024/NCKH_02-09/bert-packet-flow/model"
TOKENIZER_DIR = "/home/frblam/NCKH_2024/NCKH_02-09/bert-packet-flow/tokenizer"

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

    # Duyệt qua từng packet để dự đoán nhãn
    for packet in packets:
        try:
            labels, scores = recognize_from_packet(models, packet, flow_payload["flow_id"])
        except ValueError as e:
            # Bỏ qua packet không phải là TCP/IP
            print(f"Packet không phải là TCP/IP cho flow_id {flow_id}: {str(e)}")
            continue
        for label, score in list(zip(labels, scores))[:top_k]:
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
        average_attack_label[label] = data["total_score"] / data["count"]  # Tính trung bình

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



def main():
    model, tokenizer = load_model_and_tokenizer(MODEL_DIR, TOKENIZER_DIR)

    models = {
        "tokenizer": tokenizer,
        "model": model,
    }
    print("hello")
    count = 0
    
    #packets = read_packets_from_file('packets_hex.txt')
    # flow = read_raw_payload(collection_packets, "fl00003")
    # packets = flow["raw_payload"]
    
    flows = read_all_payload(collection_packets)
    
    
    
    # for flow in flows:
    #     fl_id = flow["flow_id"]
    #     stt = int(fl_id[2:])
    #     if stt > 561:
    #         packets = flow["raw_payload"]
    #         for packet in packets:
    #             print(fl_id)
    #             lables, scores = recognize_from_packet(models, packet, fl_id)
            
    #         print(f"flow_id : {fl_id}" ,attack_label[fl_id])
        
    #print(bert_pred_hybrid("fl00561", collection_packets))
    
    # for packet_hex in packets:
    #     count += 1
    #     if count == 800:
    #         break
    # #recognize_from_packet(models, packet_hex)
    #     print(recognize_from_packet(models, packet_hex))
        
 
    
main()