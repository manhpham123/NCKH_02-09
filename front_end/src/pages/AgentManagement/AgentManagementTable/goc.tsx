import { Card, Switch, Tooltip, Typography } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
import { useListHost} from "../../../utils/request";


const AgentManagementTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  const {data, mutate,isLoading} = useListHost(params);

  const [loadingSwitch, setLoadingSwitch] = useState<{ [key: number]: boolean }>({}); // Theo dõi trạng thái loading của từng switch


  // Hàm để xử lý sự kiện khi nhấn vào switch
  const handleSwitchChange = (checked: boolean, id: number) => {
    // Đặt trạng thái loading cho switch tương ứng với ID
    setLoadingSwitch((prev) => ({ ...prev, [id]: true }));
    
    // Sau 2s thì cập nhật trạng thái
    setTimeout(() => {
      // Xử lý logic thay đổi trạng thái của switch tại đây (nếu cần)

      // Tắt loading sau 2 giây
      setLoadingSwitch((prev) => ({ ...prev, [id]: false }));
    }, 5000);
  };

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
          <Switch
            checked={record.status === "on"}
            loading={loadingSwitch[record.id]} // Bật icon loading khi switch đang trong trạng thái loading
            onChange={(checked) => handleSwitchChange(checked, record.id)} // Gọi hàm xử lý khi switch được nhấn
          />
        </>
      ),
    },
  ];

  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Theo Dõi Máy"/>
        <TableCustom
          dataSource={data?.data}
          columns={columns}
          bordered={true}
          //isLoading={!data && isLoading}
          isLoading={isLoading}
          limit={params.limit || 10}
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

export default AgentManagementTable;