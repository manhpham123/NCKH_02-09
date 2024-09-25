from fastapi import FastAPI
#from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from data import *
import pandas as pd
import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import uvicorn
from model import *
from typing import List, Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import paramiko
from schema.file import FileNameInput, FileResponse
from test_rules_all import *



app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["cici_flow"]
db_log = client["log_json"]
db_rule = client["Rule"]

ip = "192.168.189.133"
intf_str = "ens33"
num_rows = 0

collection = db[f"flow_data_{ip}_{intf_str}"]
collection_alert = db_log["alert"]
collection_file = db_rule["rule_files"]
flowpre_collection = db[f"flow_prediction_{ip}_{intf_str}"]
collection_packets = db[f"packet_{ip}_{intf_str}"]


#file para
client_ip = "192.168.189.133"
username = "william"
password = "k"  # Thay thế "k" bằng mật khẩu thực tế


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.10.3:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Danh sách các nguồn gốc có thể truy cập API của bạn
    allow_credentials=True,
    allow_methods=["*"], # Phương thức HTTP cho phép
    allow_headers=["*"], # Tiêu đề HTTP cho phép
)

# @app.get("/items/", response_model=List[dict])
# async def read_items():
#     try:
    
        
#         # # Tiền xử lý dữ liệu
#         # df_processed = preprocess_flow(df_f)
        
#         # # Dự đoán
#         # pred = model.predict(df_processed)
        
#         # # Thêm kết quả dự đoán vào DataFrame
#         # df_f['label'] = pred
        
#         df_l = predict_label(collection)

        
#         return df_l[0:15]
        
#         # Trả về kết quả dưới dạng JSON
#         #return df_f.to_dict(orient='records')
#     except Exception as e:
#     # Nếu có lỗi, trả về thông báo lỗi với status code 500
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import paramiko
# Thay thế các thông tin dưới đây với thông tin thực tế của bạn
# host = '192.168.189.133'
# port = 22  # Port SSH mặc định
# username = 'william'
# password = 'k'
# command = '/home/william/Desktop/run_command.sh'  # Lệnh bạn muốn thực thi




# @app.post("/control/on")
# def execute_ssh_sudo_command_api(ip: str = Query(1, alias="ip")):
#     execute_ssh_sudo_command(host, port, username, password, command)
    


from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict




@app.get("/rule/alert/", response_model=List[dict])
async def get_rule_alerts ():
    alearts = read_all_data(collection_name=collection_alert)
    return alearts

@app.get("/rule/files", response_model=Dict)
async def get_file(
    page: int = Query(1, alias="page"), 
    limit: int = Query(10, alias="limit"), 
    filter_field: str = Query("", alias="filter_field"), 
    filter_value: str = Query("", alias="filter_value")
):
    try:
        # Lấy dữ liệu từ hàm get_files()
        files = get_files()

        # Nếu không có filter, phân trang dữ liệu
        if filter_field == "" or filter_value == "":
            skip = (page - 1) * limit
            
            # Tổng số bản ghi
            total = len(files)
            
            # Áp dụng phân trang
            paginated_files = files[skip: skip + limit]
            
        else:
            # Áp dụng lọc dữ liệu dựa trên filter_field và filter_value
            filtered_files = [file for file in files if file.get(filter_field) == filter_value]
            
            # Tổng số bản ghi sau khi lọc
            total = len(filtered_files)
            
            # Áp dụng phân trang cho dữ liệu đã lọc
            skip = (page - 1) * limit
            paginated_files = filtered_files[skip: skip + limit]
        
        # Đối tượng kết quả trả về
        re_ob = {
            "data": paginated_files,
            "limit": limit,
            "page": page,
            "total": total
        }
        
        # Trả về kết quả dưới dạng JSON
        return re_ob

    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/rule/alerts", response_model=Dict)
async def get_alerts_rules(
    page: int = Query(1, alias="page"), 
    limit: int = Query(10, alias="limit"), 
    filter_field: str = Query("", alias="filter_field"), 
    filter_value: str = Query("", alias="filter_value")
):
    try:
        # Lấy dữ liệu từ hàm get_files()
        files = get_alert_rules()

        # Nếu không có filter, phân trang dữ liệu
        if filter_field == "" or filter_value == "":
            skip = (page - 1) * limit
            
            # Tổng số bản ghi
            total = len(files)
            
            # Áp dụng phân trang
            paginated_files = files[skip: skip + limit]
            
        else:
            # Áp dụng lọc dữ liệu dựa trên filter_field và filter_value
            filtered_files = [file for file in files if file.get(filter_field) == filter_value]
            
            # Tổng số bản ghi sau khi lọc
            total = len(filtered_files)
            
            # Áp dụng phân trang cho dữ liệu đã lọc
            skip = (page - 1) * limit
            paginated_files = filtered_files[skip: skip + limit]
        
        # Đối tượng kết quả trả về
        re_ob = {
            "data": paginated_files,
            "limit": limit,
            "page": page,
            "total": total
        }
        
        # Trả về kết quả dưới dạng JSON
        return re_ob

    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/{md5_hash}", response_model=Dict)
async def search_md5(md5_hash: str):
    try:
        # Gọi hàm tìm kiếm
        result = search_by_md5(md5_hash)
        return result
    except HTTPException as e:
        # Trả về HTTPException nếu có lỗi
        raise e
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/line-chart-data", response_model=Dict)
async def get_chart_data():
    try: 
        threshold = 0.0001285
        pred_data = read_all_data_time(flowpre_collection, 'flow_id')
        max_mse_entry = max(pred_data, key=lambda x: x["MSE_Autoencoder"])
        data = {
            "data": pred_data,
            "max_mse": max_mse_entry["MSE_Autoencoder"],
            "threshold": threshold
        }
        # data = {
        #     "data": pred_data
        # }
        return data  
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
  

@app.get("/get_flow/", response_model=Dict)
async def get_flow(flow_id: str = Query(...)):
    try:
        flow_id = str(flow_id)
        result = get_flow_by_id(flow_id)
        return result
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/get_bert_pre/", response_model=Dict)
async def get_bert(flow_id: str = Query(...)):
    try:
        flow_id = str(flow_id)
        result = get_bert_predict(flow_id)
        return result
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
   
    
#API: http://127.0.0.1:8000/items/?page=1&limit=10&filter_field=Source%20IP&filter_value=117.18.232.200   
@app.get("/items/", response_model=Dict)
async def read_items(page: int = Query(1, alias="page"), limit: int = Query(1, alias="limit"), filter_field: str = Query("", alias="filter_field"), filter_value: str = Query("", alias="filter_value")):
    try:
        if (filter_field == "") | (filter_value == ""):
            skip = (page - 1) * limit
            # Tiền xử lý và dự đoán ở đây
            df_l, df_st = predict_label(collection)
            
            total = len(df_st)
            
            limit = limit
            
            page = page
            
            # Áp dụng phân trang
            paginated_items = df_st[skip : skip + limit]
            
            re_ob = {
                "data": paginated_items,
                "limit": limit,
                "page": page,
                "total": total
            }
            
            # Trả về kết quả dưới dạng JSON
            return re_ob
        else :
            skip = (page - 1) * limit
            # Tiền xử lý và dự đoán ở đây
            df_l, df_st = predict_label(collection)
            try:
                # Chuyển filter_value thành số nếu có thể
                if filter_value.isdigit():
                    filter_value = int(filter_value)
                else:
                    try:
                        filter_value = float(filter_value)
                    except ValueError:
                        pass  # Nếu không phải số, giữ nguyên giá trị chuỗi
            except ValueError:
                pass
            
            df_st = Filter(filter_field, filter_value, df_st)
            
            total = len(df_st)
            
            limit = limit
            
            page = page
            
            # Áp dụng phân trang
            paginated_items = df_st[skip : skip + limit]
            
            re_ob = {
                "data": paginated_items,
                "limit": limit,
                "page": page,
                "total": total
            }
            
            return re_ob
            
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
    


    
@app.get("/alert/", response_model=Dict)
async def read_alert(page: int = Query(1, alias="page"), limit: int = Query(1, alias="limit")):
    try:
        
        skip = (page - 1) * limit
        # Tiền xử lý và dự đoán ở đây
        #df_l, df_st = predict_label(collection)
        
        df_p, df_st = predict_label(collection)
        
        
        df_a = get_alert(df_st)
        
        
        total = len(df_a)
        
        limit = limit
        
        page = page
        
        # Áp dụng phân trang
        paginated_items = df_a[skip : skip + limit]
        
        re_ob = {
            "data": paginated_items,
            "limit": limit,
            "page": page,
            "total": total
        }
        
        # Trả về kết quả dưới dạng JSON
        return re_ob
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/alert/", response_model=List[dict])
# async def read_alert():
#     try:
        
#         df_l, df_st = predict_label(collection)
#         df_a = get_alert(df_st)

        
#         return df_a[-100:]
        
#         # Trả về kết quả dưới dạng JSON
#         #return df_f.to_dict(orient='records')
#     except Exception as e:
#     # Nếu có lỗi, trả về thông báo lỗi với status code 500
#         raise HTTPException(status_code=500, detail=str(e))


@app.get("/rule_files/", response_model=Dict)
async def read_file_rules(page: int = Query(1, alias="page"), limit: int = Query(1, alias="limit")):
    try:
        
        skip = (page - 1) * limit
        # doc tu rule_files 
        
        files = read_all_data(collection_file)
        

        
        
        total = len(files)
        
        limit = limit
        
        page = page
        
        # Áp dụng phân trang
        paginated_items = files[skip : skip + limit]
        
        re_ob = {
            "data": paginated_items,
            "limit": limit,
            "page": page,
            "total": total
        }
        
        # Trả về kết quả dưới dạng JSON
        return re_ob
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e)) 

@app.get("/statc/protocol", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_pro_ls = dict(sorted(static_data.pro_ls.items(), key=lambda x:x[1], reverse=True))
        
       
        return sorted_pro_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/statc/flow", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_flw_ls = dict(sorted(static_data.ip_ls.items(), key=lambda x:x[1], reverse=True))
        
        
        return sorted_flw_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
#API: http://127.0.0.1:8000/statc/service
@app.get("/statc/service", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_ser_ls = dict(sorted(static_data.service_ls.items(), key=lambda x:x[1], reverse=True))
        
        return sorted_ser_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/statc/attack", response_model=Dict)
async def static_attack():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_att_ls = dict(sorted(static_data.alert_ls.items(), key=lambda x:x[1], reverse=True))
       
        return sorted_att_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/rule_files/add_file_name")
async def add_file_name(file_input: FileNameInput):
    try:
        # Tạo document mới với timestamp hiện tại
        remote_file_path = f"/var/lib/suricata/rules/{file_input.file_name}"
        result = add_rule_file(file_input, collection_file)
        create_file_on_client(client_ip, username, password, remote_file_path, file_input.content)
        return {"status": 200, "inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/rule_file/delete/")
async def delete_file(filename: str = Query(...)):
    remote_file_path = f"/var/lib/suricata/rules/{filename}"
    response = remove_file(filename, collection_file)
    delete_file_on_client(client_ip, username, password, remote_file_path)
    if response.deleted_count > 0:
        return {"status": 200, "message": "Delete success!"}
    raise HTTPException(status_code=404, detail=f"There is no file with filename {filename}")
        
@app.get("/rule-client/get_rules/", response_model=str)
async def get_rule_file(filename: str = Query(...)):
    try:
        client_ip = "192.168.189.133"
        username = "william"
        password = "k"  # Thay thế "k" bằng mật khẩu thực tế
        remote_file_path = f"/var/lib/suricata/rules/{filename}"
        rules = read_rules_file_from_client(client_ip, username, password, remote_file_path)
       
        return rules
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/rule-client/update/",)
async def update_rule_file(filename: str = Query(...), content: str = Query(...)):
    try:
        client_ip = "192.168.189.133"
        username = "william"
        password = "k"  # Thay thế "k" bằng mật khẩu thực tế
        remote_file_path = f"/var/lib/suricata/rules/{filename}"
        rules = update_file(filename, collection_file)
        process_rules_file_on_client(client_ip, username, password, remote_file_path, content)
       
        return rules
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
