from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Tạo hoặc kết nối tới cơ sở dữ liệu
db = client['cici_flow']

# Tạo hoặc kết nối tới collection
collection = db['monitor_host']

# Dữ liệu mẫu
data = [
    {
        "id": 1,
        "hostname": "CLI_01",
        "ip": "192.168.189.133",
        "status": "off",
        "username":"william",
        "password": "k"
    },
    {
        "id": 2,
        "hostname": "CLI_02",
        "ip": "192.168.10.10",
        "status": "off",
        "username":"william",
        "password": "k"
    },
    {
        "id": 3,
        "hostname": "CLI_03",
        "ip": "192.168.189.135",
        "status": "off",
        "username":"william",
        "password": "k"
    },
    {
        "id": 4,
        "hostname": "CLI_04",
        "ip": "192.168.10.5",
        "status": "off",
        "username":"william",
        "password": "k"
    },
    {
        "id": 5,
        "hostname": "CLI_05",
        "ip": "192.168.189.128",
        "status": "off",
        "username":"william",
        "password": "k"
    },
    {
        "id": 6,
        "hostname": "CLI_06",
        "ip": "192.168.10.3",
        "status": "off",
        "username":"william",
        "password": "k"
    }
 
]

# Chèn dữ liệu vào MongoDB
collection.insert_many(data)

# Kiểm tra dữ liệu đã chèn
for machine in collection.find():
    print(machine)

# Đóng kết nối
client.close()
