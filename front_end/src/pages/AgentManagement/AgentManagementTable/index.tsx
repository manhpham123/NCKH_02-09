import { Card, Switch, Tooltip, Spin } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import { LoadingOutlined } from "@ant-design/icons"; // Import Loading Icon từ Ant Design
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
import { useListHost } from "../../../utils/request";
import { HostApi } from "../../../apis/host";

const AgentManagementTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  const { data, mutate, isLoading } = useListHost(params); // Sử dụng mutate để cập nhật lại dữ liệu

  const [loadingSwitch, setLoadingSwitch] = useState<{ [key: number]: boolean }>({}); // Theo dõi trạng thái loading của từng switch

  // Icon Loading tùy chỉnh với màu sắc
  const customLoadingIcon = (
    <LoadingOutlined style={{ fontSize: 20, color: "#e61c0e" }} spin />
  ); // Màu đỏ

  // Hàm để xử lý sự kiện khi nhấn vào switch
  const handleSwitchChange = async (checked: boolean, id: number) => {
    // Đặt trạng thái loading cho switch tương ứng với ID
    setLoadingSwitch((prev) => ({ ...prev, [id]: true }));

    try {
      // Gọi API để thay đổi trạng thái trên backend
      const res = await HostApi.ToggleStatus(id);

      // Xử lý kết quả trả về từ API nếu cần
      console.log("Response from API:", res);

      // Sau khi trạng thái thay đổi thành công, cập nhật lại danh sách host từ backend
      mutate(); // Gọi lại API để cập nhật dữ liệu từ backend
    } catch (error) {
      // Xử lý lỗi nếu có
      console.error("Failed to toggle status:", error);
    } finally {
      // Sau 1s thì tắt icon loading
      setTimeout(() => {
        setLoadingSwitch((prev) => ({ ...prev, [id]: false }));
      }, 2000);
    }
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
      title: "Địa Chỉ IP",
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
          {/* Hiển thị icon loading khi loadingSwitch[id] là true, nếu không hiển thị Switch */}
          {loadingSwitch[record.id] ? (
            <Spin indicator={customLoadingIcon} />
          ) : (
            <Switch
              checked={record.status === "on"} // Trạng thái của switch được lấy từ dữ liệu API
              onChange={(checked) => handleSwitchChange(checked, record.id)} // Gọi hàm xử lý khi switch được nhấn
            />
          )}
        </>
      ),
    },
  ];

  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Theo Dõi Máy" />
        <TableCustom
          dataSource={data?.data} // Dữ liệu sẽ tự động cập nhật sau khi mutate()
          columns={columns}
          bordered={true}
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
