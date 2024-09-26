    
    
    for file in files:  // có dữ liệu
        query = {
        "Source IP": file['dest_ip'],
        "Source Port": file['dest_port'],
        "Destination IP": file['src_ip'],
        "Destination Port": file['src_port'],
        "Protocol": protocol_name_to_number(file['protocol']),
        }
        
       for file in files:   // không có dữ liệu
        query = {
        "Source IP": file['src_ip'],
        "Source Port": file['src_port'],
        "Destination IP": file['dest_ip'],
        "Destination Port": file['dest_port'],
        "Protocol": protocol_name_to_number(file['protocol']),
        }