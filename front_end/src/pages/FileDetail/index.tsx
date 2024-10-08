import React, { FC, useEffect, useState } from "react";
import { Card, Col, Row, Typography } from "antd";
import "./style.scss";
import { useParams } from 'react-router-dom';
import { FileApi } from "../../apis/file";

const { Text, Title } = Typography;

// Định nghĩa kiểu cho đối tượng trong mảng `detections`
interface Detection {
  engine_name: string;
  result: string;
}

const FileDetails: FC = () => {
  const [dataFile, setDataFile] = useState<any | null>(null); // Đặt giá trị khởi tạo là null
  const { id } = useParams();

  const fetchDataFile = async () => {
    try {
      const res = await FileApi.GetFileDetails({ md5: id });
      setDataFile(res.data); // Lưu dữ liệu trả về vào state
    } catch (error) {
      console.error("Lỗi khi lấy chi tiết file:", error);
    }
  };

  useEffect(() => {
    fetchDataFile();
  }, [id]);
  
  if (!dataFile) {
    return <div>Đang tải dữ liệu...</div>; // Hiển thị thông báo khi dữ liệu chưa được tải
  }

  // Tách dữ liệu phát hiện thành 2 khối
  const halfLength = Math.ceil(dataFile.detections.length / 2);
  const firstHalfDetections = dataFile.detections.slice(0, halfLength);
  const secondHalfDetections = dataFile.detections.slice(halfLength);

  return (
    <div className="container-wrapper">
      <Card className="card-container" size="small">
        <h2
          style={{
            fontSize: "40px",
            fontWeight: "bold",
            textAlign: "center",
            fontFamily: "Times New Roman, Times, serif",
            marginTop: "20px",
            marginBottom: "20px",
          }}
        >
          Thông Tin Chi Tiết File
        </h2>

        {/* Row with Border */}
        <Row
          gutter={16}
          style={{
            marginBottom: 24,
            border: "1px solid #d9d9d9",
            padding: "16px",
            borderRadius: "8px",
          }}
        >
          <Col span={6}>
            <Text strong style={{ fontSize: "17px" }}>
              MD5:{" "}
            </Text>
            <Text style={{ fontSize: "17px" }}>{dataFile.hash.md5}</Text>
          </Col>
          <Col span={7}>
            <Text strong style={{ fontSize: "17px" }}>
              SHA1:{" "}
            </Text>
            <Text style={{ fontSize: "17px" }}>{dataFile.hash.sha1}</Text>
          </Col>
          <Col span={11}>
            <Text strong style={{ fontSize: "17px" }}>
              SHA256:{" "}
            </Text>
            <Text style={{ fontSize: "17px" }}>{dataFile.hash.sha256}</Text>
          </Col>
        </Row>

        {/* Another Row with Border */}
        <Row
          gutter={16}
          style={{
            marginBottom: 24,
            border: "1px solid #d9d9d9",
            padding: "16px",
            borderRadius: "8px",
          }}
        >
          <Col span={12}>
            <Title level={4}>Điểm Phát Hiện</Title>
            <Text
              type="danger"
              style={{ fontSize: "24px", fontWeight: "bold" }}
            >
              {dataFile.score}
            </Text>
          </Col>
          <Col span={12}>
            <Title level={4}>Kết quả phát hiện</Title>
            <Text style={{ fontSize: "24px", fontWeight: "bold" }}>
              {dataFile.malicious_count} / {dataFile.total_engines} Công cụ phát hiện
              độc hại
            </Text>
          </Col>
        </Row>

        {/* Hiển thị tiêu đề cho các cột hoặc thông báo "Không phát hiện thấy bất thường" */}
        {dataFile.malicious_count > 0 ? (
          <>
            {/* Tiêu đề cho các cột */}
            <Row gutter={16} style={{ marginBottom: 16 }}>
              <Col span={6}>
                <Text strong style={{ fontSize: "17px" }}>
                  Nhà cung cấp bảo mật
                </Text>
              </Col>
              <Col span={6}>
                <Text strong style={{ fontSize: "17px" }}>
                  Kết quả phát hiện
                </Text>
              </Col>
              <Col span={6}>
                <Text strong style={{ fontSize: "17px" }}>
                  Nhà cung cấp bảo mật
                </Text>
              </Col>
              <Col span={6}>
                <Text strong style={{ fontSize: "17px" }}>
                  Kết quả phát hiện
                </Text>
              </Col>
            </Row>

            {/* Dữ liệu phát hiện */}
            <Row gutter={16}>
            {firstHalfDetections.map((detection: Detection, index: number) => (
                <React.Fragment key={`row-${index}`}>
                  <Col span={6} key={`first-half-${index}`}>
                    <Text style={{ fontSize: "17px" }}>
                      {detection.engine_name}
                    </Text>
                  </Col>
                  <Col span={6} key={`first-half-result-${index}`}>
                    <Text type="danger" style={{ fontSize: "17px" }}>
                      {detection.result}
                    </Text>
                  </Col>
                  {secondHalfDetections[index] && (
                    <>
                      <Col span={6} key={`second-half-${index}`}>
                        <Text style={{ fontSize: "17px" }}>
                          {secondHalfDetections[index].engine_name}
                        </Text>
                      </Col>
                      <Col span={6} key={`second-half-result-${index}`}>
                        <Text style={{ fontSize: "17px" }} type="danger">
                          {secondHalfDetections[index].result}
                        </Text>
                      </Col>
                    </>
                  )}
                </React.Fragment>
              ))}
            </Row>
          </>
        ) : (
          <div
            style={{
              textAlign: "center",
              fontSize: "50px",
              marginTop: "20px",
            }}
          >
            <Text style={{ fontSize: "30px" }} strong>Không phát hiện thấy bất thường</Text>
          </div>
        )}
      </Card>
    </div>
  );
};

export default FileDetails;
