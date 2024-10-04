from pymongo import MongoClient
import joblib
#import torch
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler 
import warnings

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import time
from sklearn.preprocessing import normalize
#import keras
from tensorflow.keras.models import load_model
from datetime import datetime
from schema.file import FileNameInput, FileResponse
from test_bert import bert_pred, bert_pred_pt, bert_pred_stats
from check_file import get_flow_file, get_rule_alert
from virustotal import check_hash, check_hashes

protocol_numbers = {
    1: "ICMP",          # Internet Control Message Protocol
    2: "IGMP",          # Internet Group Management Protocol
    3: "GGP",           # Gateway-to-Gateway Protocol
    4: "IP-in-IP",      # IP in IP (encapsulation)
    6: "TCP",           # Transmission Control Protocol
    8: "EGP",           # Exterior Gateway Protocol
    9: "IGP",           # any private interior gateway (used by Cisco for their IGRP)
    17: "UDP",          # User Datagram Protocol
    27: "RDP",          # Reliable Datagram Protocol
    47: "GRE",          # General Routing Encapsulation
    50: "ESP",          # Encapsulating Security Payload
    51: "AH",           # Authentication Header
    57: "SKIP",         # SKIP
    58: "IPv6-ICMP",    # ICMP for IPv6
    59: "IPv6-NoNxt",   # No Next Header for IPv6
    60: "IPv6-Opts",    # Destination Options for IPv6
    88: "EIGRP",        # Enhanced Interior Gateway Routing Protocol
    89: "OSPF",         # Open Shortest Path First
    94: "IPIP",         # IP-within-IP Encapsulation Protocol
    97: "ETHERIP",      # Ethernet-within-IP Encapsulation
    98: "ENCAP",        # Encapsulation Header
    103: "PIM",         # Protocol Independent Multicast
    112: "VRRP",        # Virtual Router Redundancy Protocol
    115: "L2TP",        # Layer Two Tunneling Protocol
    132: "SCTP",        # Stream Control Transmission Protocol
    137: "MPLS-in-IP",  # MPLS-in-IP
    # Có thể thêm nhiều giao thức từ danh sách của IANA
}

port_to_protocol = {
    20: "FTP (Data)",         # File Transfer Protocol (Data Transfer)
    21: "FTP (Control)",      # File Transfer Protocol (Control)
    22: "SSH",                # Secure Shell
    23: "Telnet",             # Telnet protocol
    25: "SMTP",               # Simple Mail Transfer Protocol
    53: "DNS",                # Domain Name System
    80: "HTTP",               # Hypertext Transfer Protocol
    110: "POP3",              # Post Office Protocol v3
    143: "IMAP",              # Internet Message Access Protocol
    443: "HTTPS",             # HTTP Secure (HTTP over TLS/SSL)
    993: "IMAP SSL",          # IMAP over SSL
    995: "POP3 SSL",          # POP3 over SSL
    3306: "MySQL",            # MySQL database server
    3389: "RDP",              # Remote Desktop Protocol
    5432: "PostgreSQL",       # PostgreSQL database server
    6379: "Redis",            # Redis key-value store
    8080: "HTTP Alt",         # Alternative port for HTTP
    # Thêm các cổng và giao thức khác theo nhu cầu
}

#threshold = 0.0006894694064366165
#threshold = 0.0027183422921063186
threshold = 0.0036183422921063186

def get_protocol_name(protocol_number):
    return protocol_numbers.get(protocol_number, "Unknown")

def protocol_name_to_number(name):
    # Chuẩn hóa tên giao thức về chữ in hoa
    normalized_name = name.upper()
    
    # Duyệt qua dict để tìm số giao thức tương ứng
    for number, protocol in protocol_numbers.items():
        if protocol.upper() == normalized_name:
            return number
    
    # Nếu không tìm thấy, trả về None
    return None

def get_port_app_pro(port_number):
    return port_to_protocol.get(port_number, "Unknown")

# class thong ke
class Static:
    def __init__(self, ip_ls, pro_ls, alert_ls, service_ls):
        self.ip_ls = ip_ls
        self.pro_ls = pro_ls
        self.alert_ls = alert_ls
        self.service_ls = service_ls


       

client = MongoClient("mongodb://localhost:27017/")
db = client["cici_flow"]
db_log = client["log_json"]


#client ip
ip = "192.168.189.133"
#interface 
intf_str = "ens33"
num_rows = 0
# label_mapping = {"BENIGN": 0, "DoS Hulk": 1,'PortScan':2,'DDoS':3,'DoS GoldenEye':4,
#                  'FTP-Patator':5,'SSH-Patator':6,'DoS slowloris':7,'DoS Slowhttptest':8,'Bot':9,'Web Attack-Brute Force':10,
#                  'Web Attack-XSS':11,'Infiltration':12,'Web Attack-Sql Injection':13,'Heartbleed':14}

label_mapping = {"BENIGN": 0, "PortScan":1, "DoS slowloris": 2, "Bruce Force": 3, 'Unknown attack' : 4}
reverse_label_mapping = {value: key for key, value in label_mapping.items()}

collection = db[f"flow_data_{ip}_{intf_str}"]
flowpre_collection = db[f"flow_prediction_{ip}_{intf_str}"]
collection_alert = db_log["alert"]
collection_packets = db[f"packet_{ip}_{intf_str}"]
#load model
randomforest = joblib.load("/home/frblam/NCKH_2024/NCKH_02-09/back_end_flow/F_RandomForest/random_forest_model_27_9_cic_4label.joblib")

#model = keras.models.load_model('rfc1.md5')
autoencoder = load_model('/home/frblam/NCKH_2024/NCKH_02-09/back_end_flow/autoencoder62_09_09_53_32_12_8_new.keras')
print("okk")
T1 = 0.90
T2 = 0.0001285

#CSDL 


def get_next_id(collection_name):
    # Tìm giá trị _id lớn nhất hiện có
    latest_doc = collection_name.find_one(
        {"_id": {"$regex": "^rl"}},  # Chỉ lấy những document có _id bắt đầu bằng "rl_"
        sort=[("_id", -1)]  # Sắp xếp giảm dần theo _id để lấy document mới nhất
    )
    print(latest_doc)

    if latest_doc:
        # Lấy số hiện tại từ _id, tách phần chữ 'rl_' và chuyển thành số nguyên
        latest_id = int(latest_doc["_id"].split("l")[1])
        next_id = latest_id + 1  # Tăng giá trị _id lên 1
    else:
        # Nếu không có document nào, bắt đầu với giá trị 1
        next_id = 1

    return f"rl{str(next_id).zfill(3)}"  # Trả về _id tiếp theo theo định dạng "rl_x"

def add_rule_file(file_name : FileNameInput, collection_name):
    custom_id = get_next_id(collection_name)
    current_datetime = datetime.now()

# Định dạng ngày tháng năm theo kiểu dd-mm-yyyy
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    document = {
            "_id": custom_id,
            "filename": file_name.file_name,
            "creation_date": formatted_date
        }
        # Thêm document vào collection
    result =collection_name.insert_one(document)
    return result


def remove_file(filename, collection_name):
    result =  collection_name.delete_one({"filename": filename})
    return result

def update_file(filename, collection_name):
    current_datetime = datetime.now()

# Định dạng ngày tháng năm theo kiểu dd-mm-yyyy
    formatted_date = current_datetime.strftime("%d-%m-%Y")
    
    result = collection_name.update_one({"filename":filename}, {"$set": {"creation_date": formatted_date}})
    doc = collection_name.find_one({"filename":filename})
    return doc
    

def get_flow_by_id(flow_id):
    print(flow_id)
    flow = collection.find_one({"_id": str(flow_id)})
    predict = flowpre_collection.find_one({"flow_id": str(flow_id)})
    predict.pop("_id", None)
    combine_flow_pre = {"info": flow,
                        "pre_rf_ae":predict,
                        "threshold": T2
                        }
    return combine_flow_pre

def get_bert_predict(flow_id):
    print(flow_id)
    flow = collection.find_one({"_id": str(flow_id)})
    labels_above_threshold, total_time, total_packets = bert_pred_stats(flow_id, collection_packets)
    top = max(labels_above_threshold, key=lambda x: x["average_percentage_score"])
    top["total_time"] = total_time
    top["time_per_pac"] = total_time/total_packets
    combine_flow_pre = {"info": flow,
                        "pre_rf_ae":top
                        }
    return combine_flow_pre
   
def get_files():
    files = get_flow_file()
    flow_files = []
    print(files)
    for file in files:
        query = {
        "Source IP": file['dest_ip'],
        "Source Port": file['dest_port'],
        "Destination IP": file['src_ip'],
        "Destination Port": file['src_port'],
        "Protocol": protocol_name_to_number(file['protocol']),
        }
        print(query)
        # Tìm bản ghi khớp với điều kiện
        result = collection.find_one(query)
        if result is not None:
            file["flow_id"] = result['_id']
            flow_files.append(file)
    return flow_files 

def get_alert_rules():
    alerts = get_rule_alert()
    flow_alerts = []
    print(alerts)
    for alert in alerts:
        query = {
        "Source IP": alert['src_ip'],
        "Source Port": alert['src_port'],
        "Destination IP": alert['dest_ip'],
        "Destination Port": alert['dest_port'],
        "Protocol": protocol_name_to_number(alert['protocol']),
        }
        print(query)
        # Tìm bản ghi khớp với điều kiện
        result = collection.find_one(query)
        if result is not None:
            alert["flow_id"] = result['_id']
            flow_alerts.append(alert)
    return flow_alerts

def search_by_md5(md5_hash):
    print("md5: ",md5_hash)
    md5_hash = str(md5_hash)
    # Kết nối tới MongoDB
      # Thay thế với URL kết nối của bạn
    db = client['hash_malware']  # Thay thế với tên cơ sở dữ liệu của bạn
    collection = db['hash_md5']  # Thay thế với tên collection của bạn

    # Tìm kiếm tài liệu có hash md5 khớp
    result = collection.find_one({"hash.md5": md5_hash})

    # Kiểm tra và trả về kết quả
    if result:
        result['_id'] = str(result['_id'])
        return result
    else:
        result = check_hash(md5_hash)
        return result

def read_all_data(collection_name):
    cursor = collection_name.find().sort("flow_id", 1)

    # Chuyển đổi dữ liệu từ cursor thành danh sách các từ điển (dict)
    all_data = []
    for document in cursor:
        document["_id"] = str(document["_id"])  # Chuyển đổi ObjectId thành chuỗi
        all_data.append(document)
    
    return all_data

def read_all_data_time(collection_name, time_col):
    cursor = collection_name.find().sort(time_col, -1)

    # Chuyển đổi dữ liệu từ cursor thành danh sách các từ điển (dict)
    all_data = []
    for document in cursor:
        document["_id"] = str(document["_id"])  # Chuyển đổi ObjectId thành chuỗi
        all_data.append(document)
    
    return all_data


def FilterRead_data(filter_field, filter_value):
    """
    Đọc dữ liệu từ MongoDB và lọc theo trường cụ thể.

    :param filter_field: Trường dùng để lọc dữ liệu.
    :param filter_value: Giá trị của trường để lọc dữ liệu.
    :return: List các documents được lọc.
    """

    # Tạo filter condition
    filter_condition = {filter_field: filter_value}

    # Lọc dữ liệu và chuyển kết quả thành list
    filtered_data = list(collection.find(filter_condition))

    return filtered_data
# drop_only_nol_zero = ['Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count'
#                       , 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Fwd Avg Bytes/Bulk'
#                       , 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', ]

# drop_only_nol_inden = [ 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Header Length.1', 'Average Packet Size']




# def clear_data_only(df):
#     df.columns=df.columns.str.strip()
#     print("Dataset Shape: ",df.shape)

#     num=df._get_numeric_data()
#     num[num<0]=0

#     df.drop(columns=drop_only_nol_zero, axis=1, inplace=True)
#     print("Zero Variance Columns: ", drop_only_nol_zero, "are dropped.")
#     print("Shape after removing the zero varaince columns: ",df.shape)

#     df.replace([np.inf,-np.inf],np.nan,inplace=True)
#     print(df.isna().any(axis=1).sum(),"rows dropped")
#     df.dropna(inplace=True)
#     print("Shape after Removing NaN: ",df.shape)

#     df.drop_duplicates(inplace=True)
#     print("Shape after dropping duplicates: ",df.shape)

#     df.drop(columns=drop_only_nol_inden,axis=1,inplace=True)
#     print("Columns which have identical values: ",drop_only_nol_inden," dropped!")
#     print("Shape after removing identical value columns: ",df.shape)
#     return df
# def preprocess_autoencoder(df):
#     drop = [ 'Source IP','Destination IP', 'Source Port', 'Timestamp'
#         , 'Protocol' ,'label']
#     df.drop(columns=drop, axis=1, inplace=True)
    
#     df = clear_data_only(df)
#     index = df.index
#     print(df.info())
#     df.columns=df.columns.str.strip().str.lower().str.replace(' ','_').str.replace('(','').str.replace(')','')
#     scaler = joblib.load('minmax_scaler1.save')
#     X = scaler.transform(df)
#     return X, index
zero_variance_cols = ['Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate']
identical_cols = ['Subflow Fwd Packets', 'Subflow Bwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Header Length.1', 'Average Packet Size']
scaler_path = '/home/frblam/NCKH_2024/NCKH_02-09/back_end_flow/minmax_scaler_53_32.save'
def preprocess_autoencoder(df, scaler_path = scaler_path, zero_variance_cols = zero_variance_cols, identical_cols = identical_cols):
    """
    Xử lý dữ liệu đầu vào cho dự đoán sau khi đã huấn luyện mô hình.

    Parameters:
    - df: DataFrame chứa dữ liệu đầu vào.
    - scaler_path: Đường dẫn đến file MinMaxScaler đã được huấn luyện (định dạng .joblib).
    - zero_variance_cols: Danh sách các cột đã bị loại bỏ do phương sai bằng 0 trong quá trình huấn luyện.
    - identical_cols: Danh sách các cột đã bị loại bỏ do giá trị giống hệt nhau trong quá trình huấn luyện.

    Returns:
    - df_scaled: DataFrame đã được tiền xử lý và chuẩn hóa, sẵn sàng cho dự đoán.
    """
    drop = [ 'Source IP','Destination IP', 'Source Port', 'Timestamp'
        , 'Protocol']
    
    # Tạo một bản sao của DataFrame để không thay đổi df ban đầu
    df_processed = df.copy()
    df_processed.drop(columns=drop, axis=1, inplace=True)
    # Loại bỏ khoảng trắng ở tên cột
    df_processed.columns = df_processed.columns.str.strip()

    # Chuyển các giá trị số âm thành 0 (nếu cần thiết)
    num = df_processed._get_numeric_data()
    num[num < 0] = 0

    # Loại bỏ các cột có phương sai bằng 0 (đã biết trước)
    df_processed.drop(columns=zero_variance_cols, axis=1, inplace=True, errors='ignore')

    # Loại bỏ các cột có giá trị giống hệt nhau (đã biết trước)
    df_processed.drop(columns=identical_cols, axis=1, inplace=True, errors='ignore')

    # Xử lý giá trị vô cùng và giá trị bị thiếu (NaN)
    df_processed.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_processed.fillna(0, inplace=True)  # Thay thế giá trị NaN bằng 0 hoặc bất kỳ chiến lược nào phù hợp

    # Tải MinMaxScaler đã được huấn luyện
    scaler = joblib.load(scaler_path)

    # Áp dụng MinMaxScaler để chuẩn hóa dữ liệu
    df_scaled = scaler.transform(df_processed)

    return pd.DataFrame(df_scaled, columns=df_processed.columns)

def predict_anomalies(model , X, threshold):
    # Dự đoán output bằng autoencoder
    reconstructed = model.predict(X)
    
    # Tính reconstruction error
    reconstruction_errors = np.mean((X - reconstructed) ** 2, axis=1)
    
    # So sánh error với ngưỡng để nhận diện bất thường
    # Nếu error > threshold, đánh dấu là bất thường (1), ngược lại là bình thường (0)
    anomalies = np.where(reconstruction_errors > threshold, 4, 0)
    
    return anomalies



def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage(deep=True).sum() / 1024**2

    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()

          
            if str(col_type)[:3] == 'int':
               
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
               
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    
    end_mem = df.memory_usage(deep=True).sum() / 1024**2

   
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df



#Tien xu li du lieu 
def preprocess_flow(df_f):
    #df_f = df_f[df_f["Destination Port"]!= 443]
    #df_f = df_f[(df_f["Source Port"] != 27017) & (df_f["Destination Port"] != 27017)]
    
    # columns_to_drop = ['Source IP', 'Source Port', 'Destination IP', 'Protocol', 'Timestamp']
    # # Bỏ các cột đã chọn khỏi dataframe
    # df_f = df_f.drop(columns=columns_to_drop, axis=1)
    #df = reduce_mem_usage(df_f)
    #df.shape
    df = df_f.copy()
    train_df = df  

    stats = [] 

    for col in train_df.columns:
       
        stats.append((col,  
                    train_df[col].nunique(), 
                    train_df[col].isnull().sum() * 100 / train_df.shape[0],  
                    train_df[col].value_counts(normalize=True, dropna=False).values[0] * 100, 
                    train_df[col].dtype))  

   
    stats_df = pd.DataFrame(stats, columns=['Feature', 'Unique_values', 'Percentage of missing values', 'Percentage of values in the biggest category', 'type'])
   
    stats_df.sort_values('Percentage of missing values', ascending=False)
    df = df.dropna().reset_index(drop = True)
    df['Flow Bytes/s'].isnull().sum()

    meaningless_feature = stats_df[stats_df['Unique_values']==1]['Feature'].to_list()
    #df = df.drop(columns=meaningless_feature)
    
    inf_cols = df.max()[df.max() == np.inf].index.to_list()
    inf_cols

    for i in inf_cols:
        df[i] = df[i].apply(lambda x:100000000 if x == np.inf else x)
        
    selected_columns1 = ['Bwd Packet Length Mean', 'Total Length of Fwd Packets', 'Flow Bytes/s',
                    'Fwd Packet Length Mean', 'Subflow Fwd Bytes', 'Avg Fwd Segment Size'
                    ,'Fwd Packet Length Std', 'Flow IAT Mean',
                    'Flow IAT Max', 'Fwd IAT Mean', 'Flow Duration',
                    'Fwd Packet Length Max', 'Init_Win_bytes_backward', 'Init_Win_bytes_forward']
    
    df_sl = df[selected_columns1]

    ss = joblib.load('/home/frblam/NCKH_2024/NCKH_02-09/back_end_flow/F_RandomForest/scaler_real_cic_129 .save')
    df = ss.transform(df_sl)  
        
    return df, df_f

# Giả sử data được đọc từ hàm read_all_data(collection) và bạn đã có `data`


# Gọi hàm preprocess để tiền xử lý dữ liệu

# In DataFrame sau khi thêm cột 'label'


def predict_label(collection):
    data = read_all_data_time(collection, "Timestamp")
    df_f = pd.DataFrame(data)
    
    df_processed, df_f = preprocess_flow(df_f)
    #columns_to_drop = ['_id', 'RF']

    # # Bỏ các cột đã chọn khỏi dataframe
    # df_f = df_f.drop(columns=columns_to_drop, axis=1)
    df_pre_autoencoder= preprocess_autoencoder(df_f.drop(columns=['_id'], axis=1))  # Tiền xử lý dữ liệu cho AE
    reconstructed = autoencoder.predict(df_pre_autoencoder)
    mse_autoencoder = np.mean(np.power(df_pre_autoencoder - reconstructed, 2), axis=1)
    df_f['MSE_Autoencoder'] = 0  # Khởi tạo cột MSE
    df_f['MSE_Autoencoder'] = mse_autoencoder  # Gán MSE cho các phần tử đã tính toán
    # Thực hiện dự đoán
    pred = randomforest.predict(df_processed)
    pred_proba = randomforest.predict_proba(df_processed)  # Thêm dòng này để lấy xác suất dự đoán cho mỗi nhãn
    pred_proba_percent = (pred_proba * 100).tolist()
   
   
    pred_rf = np.array([randomforest.classes_[np.argmax(p)] if np.max(p) > T1 else 5 for p in pred_proba])
    df_f['label'] = pred_rf.astype(int)   #df_st['label'] = df_st['label'].map(reverse_label_mapping)
   
    df_f['RF'] = pred_proba_percent
    #print(pred_proba_percent)
    
    
    uncertain_indices = np.where(pred_rf == 5)[0]
    if len(uncertain_indices) > 0:
        # Gán nhãn dựa trên ngưỡng T2 cho các mẫu không chắc chắn
        pred_ae = np.where(df_f.loc[uncertain_indices, 'MSE_Autoencoder'] > T2, 4, 0)
        df_f.loc[uncertain_indices, 'label'] = pred_ae
    
    df_f = df_f[(df_f['Source IP'] != "192.168.189.128")&(df_f['Destination IP'] != "192.168.189.128")]       
    df_st = df_f[['_id','Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp', 'Flow Duration', 'label']]
    df_f['MSE_Autoencoder'] = df_f['MSE_Autoencoder'].apply(lambda x: 0.001 if pd.isna(x) else x)
    df_st['label'] = df_st['label'].map(reverse_label_mapping).astype('str')
    #print(df_f['label'])
    update_database_with_predictions(df_f)
    df_f.drop(columns='MSE_Autoencoder', axis=1)
    
    return df_f.to_dict(orient='records'), df_st.to_dict(orient='records')
    #return df_f

def update_database_with_predictions(df_f):
    """
    Cập nhật dự đoán vào MongoDB.

    Args:
        df_f (DataFrame): Dữ liệu với các dự đoán để cập nhật vào MongoDB.
    """
    # Tìm flow_id cuối cùng đã tồn tại trong collection
    last_document = flowpre_collection.find_one(sort=[("flow_id", -1)])  # Tìm document cuối cùng theo flow_id
    last_flow_id = last_document['flow_id'] if last_document else None  # Lấy flow_id cuối cùng, nếu không có thì là None
    
    # Chạy vòng lặp qua từng hàng trong dataframe df_f
    for index, row in df_f.iterrows():
        flow_id = row['_id'] if '_id' in row else index  # Giả sử '_id' là ID duy nhất trong MongoDB hoặc sử dụng 'index' nếu không có
        # Chỉ thêm dữ liệu nếu flow_id của dòng hiện tại lớn hơn last_flow_id
        if last_flow_id is None or flow_id > last_flow_id:
            # Nếu last_flow_id là None (không có bản ghi nào trước đó) hoặc flow_id lớn hơn last_flow_id
            flowpre_collection.insert_one({
                'flow_id': flow_id,
                "normal": row["RF"][0],
                "portscan": row["RF"][1],
                "dos_slowloris": row["RF"][2],  # Chứa xác suất dự đoán của Random Forest (dưới dạng phần trăm)
                "bruce_force" : row["RF"][3],
                'MSE_Autoencoder': row['MSE_Autoencoder'],
                "time": row["Timestamp"]  # Chứa MSE của Autoencoder
            })    
    

results = search_by_md5('b94af4a4d4af6eac81fc135abda1c40c')
print(results)
# def predict_label(collection):
#     data = read_all_data(collection)
#     df_f = pd.DataFrame(data)
#     df_processed, df_f = preprocess_flow(df_f)
#     columns_to_drop = ['_id', 'RF']

#     # # Bỏ các cột đã chọn khỏi dataframe
#     # df_f = df_f.drop(columns=columns_to_drop, axis=1)
    
#     # Thực hiện dự đoán
#     pred = randomforest.predict(df_processed)
#     pred_proba = randomforest.predict_proba(df_processed)  # Thêm dòng này để lấy xác suất dự đoán cho mỗi nhãn
#     pred_proba_percent = (pred_proba * 100).tolist()
   
   
#     df_f['label'] = pred
#     #df_st['label'] = pred
#     df_f['label'] = df_f['label'].map(reverse_label_mapping)
#     #df_st['label'] = df_st['label'].map(reverse_label_mapping)
   
#     df_f['RF'] = pred_proba_percent
#     print(pred_proba_percent)
    
    
#     #AE-mse
#     df_pre_autoencoder, index = preprocess_autoencoder(df_f.drop(columns=columns_to_drop, axis=1))
#     pred_autoencoder = autoencoder.predict(df_pre_autoencoder)  # Dự đoán đầu ra của Autoencoder

#     # Tính Mean Squared Error (MSE) cho từng dòng
#     mse_autoencoder = np.mean(np.power(df_pre_autoencoder - pred_autoencoder, 2), axis=1)
#     df_f.loc[index ,'MSE_Autoencoder'] = mse_autoencoder
    
    
#     df_benign = df_f[df_f['label'] == 'BENIGN']
#     columns_to_drop_be = ['_id', 'RF', 'MSE_Autoencoder']
#     df_benign = df_benign.drop(columns=columns_to_drop_be, axis=1)
    
#     #df_benign.loc[(df_benign["Source Port"] == 27017) &( df_benign["Destination Port"] == 27017), "label"] = 'BENIGN'
#     if df_benign.shape[0] > 0:
    
#         df_pre, index = preprocess_autoencoder(df_benign)
        
#         pred_au = predict_anomalies(autoencoder,df_pre, threshold)
        
#         print(pred_au)
        
#         vectorized_map = np.vectorize(reverse_label_mapping.get)

#     # Áp dụng ánh xạ cho mảng
#         pred_au = vectorized_map(pred_au)
        
#         #pred_au = pred_au.map(reverse_label_mapping)
        
#         df_f.loc[index, 'label'] = pred_au
        
#         # df_f.loc[(df_f["Source Port"] == 27017) | 
#         #   (df_f["Destination Port"] == 27017) | 
#         #   ((df_f["Destination IP"] != "192.168.10.5") & 
#         #  (df_f["Destination IP"] != "192.168.10.10")), 'label'] = "BENIGN"
    
    
#     df_st = df_f[['Source IP', 'Source Port', 'Destination IP', 'Destination Port', 'Protocol', 'Timestamp', 'Flow Duration', 'label']]

#     df_f['MSE_Autoencoder'] = df_f['MSE_Autoencoder'].apply(lambda x: 0.001 if pd.isna(x) else x)
#     # Tìm flow_id cuối cùng đã tồn tại trong collection
#     last_document = flowpre_collection.find_one(sort=[("flow_id", -1)])  # Tìm document cuối cùng theo flow_id
#     last_flow_id = last_document['flow_id'] if last_document else None  # Lấy flow_id cuối cùng, nếu không có thì là None
#     # Chạy vòng lặp qua từng hàng trong dataframe df_f
#     for index, row in df_f.iterrows():
#         flow_id = row['_id'] if '_id' in row else index  # Giả sử '_id' là ID duy nhất trong MongoDB hoặc sử dụng 'index' nếu không có
#     # Chỉ thêm dữ liệu nếu flow_id của dòng hiện tại lớn hơn last_flow_id
#         if last_flow_id is None or flow_id > last_flow_id:
     
#             # Nếu last_flow_id là None (không có bản ghi nào trước đó) hoặc flow_id lớn hơn last_flow_id
#             # flowpre_collection.insert_one({
#             #     'flow_id': flow_id,
#             #     "PortScan": row["RF"]["PortScan"],
#             #     "DoS slowloris": row["RF"]["DoS slowloris"],  # Chứa xác suất dự đoán của Random Forest (dưới dạng phần trăm)
#             #     "Bruce Force" : row["RF"]["Bruce Force"],
#             #     'MSE_Autoencoder': row['MSE_Autoencoder']  # Chứa MSE của Autoencoder
#             # })
          
#              flowpre_collection.insert_one({
#                 'flow_id': flow_id,
#                 "normal": row["RF"][0],
#                 "portscan": row["RF"][1],
#                 "dos_slowloris": row["RF"][2],  # Chứa xác suất dự đoán của Random Forest (dưới dạng phần trăm)
#                 "bruce_force" : row["RF"][3],
#                 'MSE_Autoencoder': row['MSE_Autoencoder'],
#                 "time": row["Timestamp"]# Chứa MSE của Autoencoder
#             })

#     #print(df_f)
#     df_f.drop(columns='MSE_Autoencoder', axis=1)
    
#     return df_f.to_dict(orient='records'), df_st.to_dict(orient='records')
df_p, df_st = predict_label(collection)

# ham thong ke
def get_ls(df_st):
    service_ls = {}
    pro_ls = {}
    ip_ls = {}
    alert_ls = {}
    st1 = Static(pro_ls, ip_ls, alert_ls, service_ls) 
    
    for d in df_st:
        if get_protocol_name(int(d['Protocol'])) not in st1.pro_ls.keys():
            st1.pro_ls[get_protocol_name(int(d['Protocol']))] = 0
            
        if get_protocol_name(int(d['Protocol'])) in st1.pro_ls.keys():
            st1.pro_ls[get_protocol_name(int(d['Protocol']))] += 1
    
        if get_port_app_pro(int(d['Destination Port'])) not in st1.service_ls.keys():
            st1.service_ls[get_port_app_pro(int(d['Destination Port']))] = 0
            
        if get_port_app_pro(int(d['Destination Port'])) in st1.service_ls.keys():
            st1.service_ls[get_port_app_pro(int(d['Destination Port']))] += 1
        
        if d['Source IP']+'-'+d['Destination IP'] not in st1.ip_ls.keys():
            st1.ip_ls[d['Source IP']+'-'+d['Destination IP']] = 0
            
        if d['Source IP']+'-'+d['Destination IP'] in st1.ip_ls.keys():
            st1.ip_ls[d['Source IP']+'-'+d['Destination IP']] += 1
        
        if d['label'] != "BENIGN":
            
            if d['label'] not in st1.alert_ls.keys():
                st1.alert_ls[d['label']] = 0
            
            if d['label'] in st1.alert_ls.keys():
                st1.alert_ls[d['label']] += 1
    
    return st1


def Filter(field, value, df_st):
    filter_data = []
    
    print(field, ':', value)
    for d in df_st:
        if d[field] == value:
            filter_data.append(d)
            print(field, ':', value)      
    return filter_data

#du doan bat thuong
def get_alert (df_st):
    l_df_a = []
    sum_sql_dos = 0
    sum_sql = 0
    for row in df_st:
        if row['label'] != 'BENIGN' : 
            #row['label'] = row['label'].map(label_mapping)
            l_df_a.append(row)
            # print(row['label'])
            # print(len(l_df_a))
    #     if row["Destination Port"] == 27017 and row['label'] != 'BENIGN':
    #         sum_sql_dos += 1
    #     if row["Destination Port"] == 27017:
    #         sum_sql += 1
    # print(sum_sql_dos)
    #print(sum_sql_dos/sum_sql)   
    return l_df_a
   
# flow = get_flow_by_id("fl00001")
# print(flow)
#print(read_all_data(collection_name=collection_alert))     
# kq =  get_alert(df_st)
# print(kq)

# st2 = get_ls(df_st)

# # print(st2.ip_ls)
# print(st2.pro_ls)
# # print(st2.service_ls)

# field = 'Protocol'
# value = 17

#print(Filter(field, value, df_st))

# all_data = read_all_data(collection)

# print(all_data)