    for alert in alerts:   // hiện ít dữ liệu
        query = {
        "Source IP": alert['src_ip'],
        "Source Port": alert['src_port'],
        "Destination IP": alert['dest_ip'],
        "Destination Port": alert['dest_port'],
        "Protocol": protocol_name_to_number(alert['protocol']),
        }
        
        
        
        for alert in alerts:   // hiện nhiều dữ liệu hơn
        query = {
        "Source IP": alert['dest_ip'],
        "Source Port": alert['dest_port'],
        "Destination IP": alert['src_ip'],
        "Destination Port": alert['src_port'],
        "Protocol": protocol_name_to_number(alert['protocol']),
        }