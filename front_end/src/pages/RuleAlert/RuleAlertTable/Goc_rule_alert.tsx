import { Button, Card, Tooltip, Typography, Modal } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
import { useCheckFile } from "../../../utils/request";
import ListButtonActionUpdate from "../../../components/ListButtonActionUpdate";

const RuleAlertTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  // const {data, mutate,isLoading} = useCheckFile(params);
  const isLoading =  false;
  const data = {
    "data": [
      {
        "timestamp": "2024-09-14T16:41:49.484373+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 50516,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER SELECT USER SQL Injection Attempt in URI",
        "signature_id": 2010963,
        "severity": 1,
        "flow_id": "fl01355"
      },
      {
        "timestamp": "2024-09-14T16:41:54.731832+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 50528,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER Script tag in URI Possible Cross Site Scripting Attempt",
        "signature_id": 2009714,
        "severity": 1,
        "flow_id": "fl01358"
      },
      {
        "timestamp": "2024-09-14T16:41:59.865337+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 34930,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER Onmouseover= in URI - Likely Cross Site Scripting Attempt",
        "signature_id": 2009715,
        "severity": 1,
        "flow_id": "fl01359"
      },
      {
        "timestamp": "2024-09-14T16:42:05.445389+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 34940,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER Possible MySQL SQLi Attempt Information Schema Access",
        "signature_id":2017808,
        "severity": 1,
        "flow_id": "fl01360"
      },
      {
        "timestamp": "2024-09-14T16:42:10.835213+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 52748,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER ATTACKER SQLi - SELECT and Schema Columns M1",
        "signature_id": 2017337,
        "severity": 1,
        "flow_id": "fl01362"
      },
      {
        "timestamp": "2024-09-14T16:42:16.668305+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 52756,
        "protocol": "TCP",
        "signature": "SURICATA QUIC failed decrypt",
        "signature_id": 2231000,
        "severity": 3,
        "flow_id": "fl01363"
      },
      {
        "timestamp": "2024-09-14T16:42:21.963465+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 40986,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER SQL Errors in HTTP 200 Response (error in your SQL syntax)",
        "signature_id": 2016672,
        "severity": 2,
        "flow_id": "fl01364"
      },
      {
        "timestamp": "2024-09-14T16:42:27.425488+0000",
        "src_ip": "192.168.189.135",
        "src_port": 80,
        "dest_ip": "192.168.189.133",
        "dest_port": 40992,
        "protocol": "TCP",
        "signature": "ET WEB_SERVER SELECT USER SQL Injection Attempt in URI",
        "signature_id": 2010963,
        "severity": 1,
        "flow_id": "fl01365"
      }
    ],
    "limit": 10,
    "page": 1,
    "total": 8
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  const ChiTietRule = () => {
    window.location.href = 'http://localhost:3001/#/alerts/26985';
  };
 
  const columns: ColumnsType<any> = [
    {
      key: 1,
      title: "Số Thứ Tự",
      align: "center",
      width: "7%",
      render: (_, record, index) => {
        return index + 1;
      },
    },
    {
      key: 2,
      title: "Flow ID",
      dataIndex: "flow_id",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 3,
      title: "Thời Gian",
      dataIndex: "timestamp",
      align: "center",
      render: (timestamp) => (
        <Tooltip title={formatDate(timestamp)}>
          <div className="inline-text">{formatDate(timestamp)}</div>
        </Tooltip>
      ),
    },
    {
      key: 4,
      title: "signature",
      dataIndex: "signature",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    
    {
      key: 5,
      title: "signature_id",
      dataIndex: "signature_id",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    /*
    {
      key: 5,
      title: "SHA1",
      dataIndex: "sha1",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 6,
      title: "SHA256",
      dataIndex: "sha256",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    */
    {
      key: 6,
      title: "Mức Độ",
      dataIndex: "severity",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    /*
    {
      key: 7,
      title: "Source IP",
      dataIndex: "src_ip",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 8,
      title: "Source Port",
      dataIndex: "src_port",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 9,
      title: "Destination IP",
      dataIndex: "dest_ip",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 10,
      title: "Destination Port",
      dataIndex: "dest_port",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    */
    {
      key: 11,
      title: "Chi Tiết Flow",
      align: "center",
      width: "8%",
      render: (_, record) => (
        <>
          <ListButtonActionUpdate
            // editFunction={() => {}}
            viewFunction={() =>  navigate(`/flow-details/${record.flow_id}`)}
          />
        </>
      ),
    },
    {
      key: 12,
      title: "Chi Tiết Rule",
      align: "center",
      width: "8%",
      render: (_, record) => (
        <>
          <ListButtonActionUpdate
            
            viewFunction={ChiTietRule}
          />
        </>
      ),
    }
  ];
 


  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Rule Alert"/>
        <TableCustom
          dataSource={data?.data}
          columns={columns}
          bordered={true}
          isLoading={isLoading}
          limit={params.limit || 15 }
          total={data?.total}
          onLimitChange={(limit) => {
            setParams({ ...params, limit });
          }}
          onPageChange={(page) => {
            setParams({ ...params, page });
          }}
          page={params.page || 1}
        />
      </Card>
    </div>
  );
};

export default RuleAlertTable;
