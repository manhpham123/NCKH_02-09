import { Button, Card, Tooltip, Typography } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";

import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";

const CheckFileTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });

  const isLoading = false;
  const data = {
    "data": [
      // Dữ liệu mock của bạn
    ],
    "limit": 10,
    "page": 1,
    "total": 100
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
      title: "Tên File",
      dataIndex: "filename",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 3,
      title: "MD5",
      dataIndex: "md5",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 4,
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
      key: 5,
      title: "SHA256",
      dataIndex: "sha256",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 6,
      title: "Kích Thước",
      dataIndex: "size",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 7,
      title: "Hành Động",
      align: "center",
      width: "20%",
      render: (_, record) => (
        <div>
          <Button
            type="primary"
            style={{ marginRight: 8 }}
            onClick={() => handleCheckDb(record.md5)}
          >
            Check DB
          </Button>
          <Button
            type="default"
            onClick={() => handleCheckVirusTotal(record.md5)}
          >
            Check VirusTotal
          </Button>
        </div>
      ),
    },
  ];

  const handleCheckDb = (md5: string) => {
    console.log("Check DB với mã MD5:", md5);
    // Thêm logic xử lý khi nhấn "Check DB"
  };

  const handleCheckVirusTotal = (md5: string) => {
    console.log("Check VirusTotal với mã MD5:", md5);
    // Thêm logic xử lý khi nhấn "Check VirusTotal"
  };

  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Check File" />
        <TableCustom
          dataSource={data?.data}
          columns={columns}
          bordered={true}
          isLoading={isLoading}
          limit={params.limit || 15}
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

export default CheckFileTable;
