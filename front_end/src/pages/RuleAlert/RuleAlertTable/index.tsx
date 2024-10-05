import { Button, Card, Tooltip, Typography, Modal } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
import { useRuleAlert} from "../../../utils/request";
import ListButtonActionUpdate from "../../../components/ListButtonActionUpdate";

const RuleAlertTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  const {data, mutate,isLoading} = useRuleAlert(params);
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

  const ChiTietRule = (_id: number) => {
    // window.location.href = `http://localhost:3001/#/alerts/${_id}`;
    window.open(`http://localhost:3001/#/alerts/${_id}`, '_blank');

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
          viewFunction={() => {
            const newWindow = window.open(`/flow-details/${record._id}`, '_blank');
            if (newWindow) {
              newWindow.focus();
            }
          }}
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
          viewFunction={() => ChiTietRule(record._id)}
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
