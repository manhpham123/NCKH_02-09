import { FC, useEffect, useState } from "react";
import { Card, Col, Row, Typography } from "antd";
import "./style.scss";
import CardTitleCustom from "../../components/CardTitleCustom";
import { useParams } from 'react-router-dom';
import { FileApi } from "../../apis/file";

const { Text, Title } = Typography;

const FileDetails: FC = () => {
  const [dataFile, setDataFile] = useState<any[]>([]);
  const { id } = useParams();

  const fetchDataFile = async () => {
    const res = await FileApi.GetFileDetails({ md5: id });
    // Xử lý dữ liệu và cập nhật state
  };

  useEffect(() => {
    fetchDataFile();
  }, [id]);

  //===================== Dữ liệu mẫu===========================
  const data = {
    
    "hash": {
      "md5": "486868aae425e458c56a5a4c6a9fbcf2",
      "sha1": "ee4b2a2a5992127b71678e82b72d574e54ded8b4",
      "sha256": "c8440d0baf8343ef5e692d5b09ef495aa4532c9c88cdf1cffd37064e7e1704ed"
    },
    "score": "32/59",
    "malicious_count": 32,
    "total_engines": 59,
    "detections": [
      {
        "engine_name": "Cynet",
        "result": "Malicious (score: 85)"
      },
      {
        "engine_name": "FireEye",
        "result": "Application.BitCoinMiner.AJF"
      },
      {
        "engine_name": "CAT-QuickHeal",
        "result": "Coinhive.Miner.30698"
      },
      {
        "engine_name": "McAfee",
        "result": "JS/Miner.ck"
      },
      {
        "engine_name": "Zillya",
        "result": "Trojan.CoinMiner.JS.3"
      },
      {
        "engine_name": "Sangfor",
        "result": "Malware"
      },
      {
        "engine_name": "Invincea",
        "result": "Coinhive JavaScript cryptocoin miner (PUA)"
      },
      {
        "engine_name": "TrendMicro-HouseCall",
        "result": "Coinminer_COINHIVE.SMF1-JS"
      },
      {
        "engine_name": "Avast",
        "result": "JS:Miner-AF [PUP]"
      },
      {
        "engine_name": "ClamAV",
        "result": "Js.Coinminer.Generic-6836639-1"
      },
      {
        "engine_name": "BitDefender",
        "result": "Application.BitCoinMiner.AJF"
      },
      {
        "engine_name": "NANO-Antivirus",
        "result": "Riskware.Script.Miner.fmbqgs"
      },
      {
        "engine_name": "MicroWorld-eScan",
        "result": "Application.BitCoinMiner.AJF"
      },
      {
        "engine_name": "Rising",
        "result": "Trojan.CoinHive!1.B2E9 (CLASSIC)"
      },
      {
        "engine_name": "Ad-Aware",
        "result": "Application.BitCoinMiner.AJF"
      },
      {
        "engine_name": "Emsisoft",
        "result": "Application.BitCoinMiner.AJF (B)"
      },
      {
        "engine_name": "Comodo",
        "result": "Application.JS.CoinMiner.RA@7u1yex"
      },
      {
        "engine_name": "F-Secure",
        "result": "PotentialRisk.PUA/CryptoMiner.Gen"
      },
      {
        "engine_name": "DrWeb",
        "result": "JS.Miner.11"
      },
      {
        "engine_name": "TrendMicro",
        "result": "Coinminer_COINHIVE.SMF1-JS"
      },
      {
        "engine_name": "Sophos",
        "result": "Coinhive JavaScript cryptocoin miner (PUA)"
      },
      {
        "engine_name": "Ikarus",
        "result": "PUA.CoinMiner"
      },
      {
        "engine_name": "Jiangmin",
        "result": "Trojan.Script.Generic1"
      },
      {
        "engine_name": "Avira",
        "result": "PUA/CryptoMiner.Gen"
      },
      {
        "engine_name": "Antiy-AVL",
        "result": "Trojan[Infect]/JS.Miner"
      },
      {
        "engine_name": "Microsoft",
        "result": "Trojan:Script/Wacatac.C!ml"
      },
      {
        "engine_name": "Arcabit",
        "result": "Application.BitCoinMiner.AJF"
      },
      {
        "engine_name": "GData",
        "result": "Script.Application.CoinHive.A"
      },
      {
        "engine_name": "Tencent",
        "result": "Html.Win32.Script.504241"
      },
      {
        "engine_name": "MAX",
        "result": "malware (ai score=82)"
      },
      {
        "engine_name": "Fortinet",
        "result": "JS/Miner.CK!tr"
      }
    ]
  }

  // Tách dữ liệu phát hiện thành 2 khối
  const halfLength = Math.ceil(data.detections.length / 2);
  const firstHalfDetections = data.detections.slice(0, halfLength);
  const secondHalfDetections = data.detections.slice(halfLength);

  return (
    <div className="container-wrapper">
      <Card className="card-container" size="small">
        {/* Adjusted Title with Custom Style */}
        {/* <div style={{ marginTop: '20px', marginBottom: '20px' }}>
          <CardTitleCustom title="File Details" />
        </div> */}
               {/* Sử dụng thẻ h2 thay thế cho CardTitleCustom */}
        <h2 style={{ fontSize: '40px', fontWeight: 'bold', textAlign: 'center', fontFamily: 'Times New Roman, Times, serif', marginTop: '20px', marginBottom: '20px' }}>
        Thông Tin Chi Tiết File
        </h2>
       

        {/* Row with Border */}
        <Row gutter={16} style={{ marginBottom: 24, border: '1px solid #d9d9d9', padding: '16px', borderRadius: '8px' }}>
          <Col span={6}>
            <Text strong style={{ fontSize: '17px' }}>MD5: </Text>
            <Text style={{ fontSize: '17px' }}>{data.hash.md5}</Text>
          </Col>
          <Col span={7}>
            <Text strong style={{ fontSize: '17px' }}>SHA1: </Text>
            <Text style={{ fontSize: '17px' }}>{data.hash.sha1}</Text>
          </Col>
          <Col span={11}>
          <Text strong style={{ fontSize: '17px' }}>SHA256: </Text>
          <Text style={{ fontSize: '17px' }}>{data.hash.sha256}</Text>
          </Col>
        </Row>

        {/* Another Row with Border */}
        <Row gutter={16} style={{ marginBottom: 24, border: '1px solid #d9d9d9', padding: '16px', borderRadius: '8px' }}>
          <Col span={12}>
            <Title level={4}>Điểm Phát Hiện</Title>
            <Text type="danger" style={{ fontSize: '24px', fontWeight: 'bold' }}>{data.score}</Text>
          </Col>
          <Col span={12}>
            <Title level={4}>Kết quả phát hiện</Title>
            <Text style={{ fontSize: '24px', fontWeight: 'bold' }}>{data.malicious_count} / {data.total_engines} Công cụ phát hiện độc hại</Text>
          </Col>
        </Row>

        {/* Tiêu đề cho các cột */}
        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Text strong style={{ fontSize: '17px' }}>Nhà cung cấp bảo mật</Text>
          </Col>
          <Col span={6}>
            <Text strong style={{ fontSize: '17px' }}>Kết quả phát hiện</Text>
          </Col>
          <Col span={6}>
            <Text strong style={{ fontSize: '17px' }}>Nhà cung cấp bảo mật</Text>
          </Col>
          <Col span={6}>
            <Text strong style={{ fontSize: '17px' }}>Kết quả phát hiện</Text>
          </Col>
        </Row>

        {/* Dữ liệu phát hiện */}
   {/* Bảng dữ liệu phát hiện với viền bao bọc và đường viền ngang giữa các hàng */}
   <div style={{ border: '1px solid #d9d9d9', borderRadius: '8px', padding: '16px', marginTop: '30px' }}>
          <Row gutter={16}>
            {firstHalfDetections.map((detection, index) => (
              <Row
                gutter={16}
                key={`row-${index}`}
                style={{
                  borderBottom: index !== firstHalfDetections.length - 1 ? '1px solid #f0f0f0' : 'none', // Đường kẻ ngang phân biệt các dòng trừ dòng cuối
                  padding: '8px 0' // Khoảng cách trên và dưới mỗi dòng
                }}
              >
                <Col span={6} key={`first-half-${index}`}>
                  <Text style={{ fontSize: '17px' }}>{detection.engine_name}</Text>
                </Col>
                <Col span={6} key={`first-half-result-${index}`}>
                  <Text type="danger" style={{ fontSize: '17px' }}>{detection.result}</Text>
                </Col>
                {secondHalfDetections[index] && (
                  <>
                    <Col span={6} key={`second-half-${index}`}>
                      <Text style={{ fontSize: '17px' }}>{secondHalfDetections[index].engine_name}</Text>
                    </Col>
                    <Col span={6} key={`second-half-result-${index}`}>
                      <Text style={{ fontSize: '17px' }} type="danger">{secondHalfDetections[index].result}</Text>
                    </Col>
                  </>
                )}
              </Row>
            ))}
          </Row>
        </div>
      </Card>
    </div>
  );
};

export default FileDetails;
