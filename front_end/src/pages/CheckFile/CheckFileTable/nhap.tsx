import { Button, Card, Tooltip, Typography, Modal } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";

import "./style.scss"; // Bổ sung thêm CSS của bạn vào đây
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
    data: [
      //... dữ liệu file mẫu
    ],
    limit: 10,
    page: 1,
    total: 100,
  };

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState<JSX.Element | null>(null);

  const showModal = (content: JSX.Element) => {
    setModalContent(content);
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  const columns: ColumnsType<any> = [
    //... Các cột của bảng như trong mã gốc
  ];

  const handleCheckDb = (md5: string) => {
    // Dữ liệu mẫu trả về thành công
    const response = {
      status: "success",
      name: "Trojan.Win32.Emotet.471040.A",
    };

    if (response.status === "success") {
      showModal(
        <div>
          <Typography.Title level={4}>Kiểm Tra File Thành Công</Typography.Title>
          <p style={{ fontWeight: "normal" }}>
            <strong>Kết quả phát hiện:</strong>{" "}
            <span style={{ color: "red" }}>{response.name}</span>
          </p>
          <p style={{ fontWeight: "normal" }}>Thông tin về file được tìm thấy trong cơ sở dữ liệu.</p>
        </div>
      );
    } else {
      showModal(
        <div>
          <Typography.Title level={4}>Kiểm Tra File Thất Bại</Typography.Title>
          <p style={{ fontWeight: "normal" }}>Không tìm thấy thông tin file trong cơ sở dữ liệu.</p>
        </div>
      );
    }
  };

  const handleCheckVirusTotal = (md5: string) => {
    showModal(
      <div>
        <Typography.Title level={4}>Check VirusTotal</Typography.Title>
        <p style={{ fontWeight: "normal" }}>MD5: {md5}</p>
        <p style={{ fontWeight: "normal" }}>Thêm nội dung modal ở đây...</p>
      </div>
    );
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
      <Modal
        title="Thông Tin Kiểm Tra"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={600} // Tăng kích thước modal
        style={{ borderRadius: "10px", overflow: "hidden" }} // Thêm phong cách cho modal
      >
        {modalContent}
      </Modal>
    </div>
  );
};

export default CheckFileTable;
