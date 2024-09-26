import { Card, Switch, Tooltip, Typography } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
const AgentManagementTable: FC = () => {
  const navigate = useNavigate();

/*================ DU LIEU MAU, backend tra ve dang nay=============*/
const [params, setParams] = useState<CommonGetAllParams>({
  limit: 10,
  page: 1,
});
const isLoading = false
const DanhSachHost = {
  "data": 
  [
    {
      "id": 1,
      "hostname": "CLI_01",
      "ip": "192.168.189.133",
      "status": "on"
  },
  {
      "id": 2,
      "hostname": "CLI_02",
      "ip": "192.168.10.10",
      "status": "off"
  },
  {
      "id": 3,
      "hostname": "CLI_03",
      "ip": "192.168.189.135",
      "status": "off"
  },
  {
      "id": 4,
      "hostname": "CLI_04",
      "ip": "192.168.10.5",
      "status": "off"
  },
  {
      "id": 5,
      "hostname": "CLI_05",
      "ip": "192.168.189.128",
      "status": "off"
  },
  {
      "id": 6,
      "hostname": "CLI_06",
      "ip": "192.168.10.3",
      "status": "off"
  }
  ],
      "limit": 5,
      "page": 1,
      "total": 5
  }

  const columns: ColumnsType<any> = [
    {
      key: 1,
      title: "Số Thứ Tự",
      align: "center",
      width: "10%",
      render: (_, record, index) => {
        return index + 1;
      },
    },
    {
      key: 2,
      title: "Tên Máy",
      dataIndex: "hostname",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 3,
      title: "Địa Chỉ IP  ",
      dataIndex: "ip",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 4,
      title: "Thu Thập Dữ Liệu",
      align: "center",
      width: "10%",
      render: (_, record) => (
        <>
        <Switch defaultChecked={record.status === "on"} />
      </>
      ),
    }
  ];
 

  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Danh Sách Các Máy Theo Dõi"/>
        <TableCustom
          dataSource={DanhSachHost?.data}
          columns={columns}
          bordered={true}
          //isLoading={!data && isLoading}
          isLoading={isLoading}
          limit={DanhSachHost.limit || 10}
          total={DanhSachHost?.total}
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

export default AgentManagementTable;
