import { Card } from "antd";
import { FC } from "react";
import "./style.scss";
import TableBert from "../../components/TableBert";
import { Col, Row } from "antd";

const RuleAlertTable: FC = () => {
  const data = {
    "label": "Web Attack - SQL INJECTION",
    "average_percentage_score": "95.1577438967",
    "packet_ratio": "8/25",
    "total_time": "4.130246162",
    "time_per_pac": "0.4531930073"
  };

  // Tiêu đề tùy chỉnh cho từng hàng
  const customFields = {
    "label": "Nhãn dự đoán",
    "average_percentage_score": "Tỷ lệ phần trăm dự đoán trung bình (%)",
    "packet_ratio": "Số gói tin",
    "total_time": "Tổng thời gian",
    "time_per_pac": "Thời gian/gói tin"
  };

  return (
    <div className="container-wrapper">
      <Card className="card-container" size="small">
        {/* Căn giữa tiêu đề bằng cách sử dụng style */}
        <h2 style={{ marginBottom: '20px', marginLeft: '250px' }}>DỰ ĐOÁN BERT</h2>
        <Row gutter={[12, 12]}>
          {/* Bảng ở bên trái */}
          <Col span={10}>
            <div className="table-container">
              <TableBert data={data} customFields={customFields} />
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default RuleAlertTable;
