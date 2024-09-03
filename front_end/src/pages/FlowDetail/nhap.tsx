import { FC, useEffect, useState } from "react";
import { Card, Col, Row, Button, Typography } from "antd";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import SimpleTable from "../../components/SimpleTable";
import CardTitleCustom from "../../components/CardTitleCustom";
import { useParams } from 'react-router-dom';
import { FlowApi } from "../../apis/flow";
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

const { Text } = Typography;

const FlowDetails: FC = () => {
  const [dataFlow, setDataFlow] = useState<any[]>([]);
  const [preRfAeData, setPreRfAeData] = useState<any>({});
  const [bertData, setBertData] = useState<any>({});
  const { id } = useParams();

  const fetchDataFlow = async () => {
    const res = await FlowApi.GetFlowDetails({ flow_id: id });
    const info = res.data.info;
    const data = Object.entries(info).map(([key, value]) => ({ key, value }));
    setDataFlow(data);

    // Fetch additional data for pre_rf_ae and bert
    setPreRfAeData(res.data.pre_rf_ae);
    setBertData(res.data.bert);
  };

  useEffect(() => {
    fetchDataFlow();
  }, [id]);

  const columns: ColumnsType<any> = [
    {
      title: 'Trường',
      dataIndex: 'key',
      key: 'key',
    },
    {
      title: 'Giá Trị',
      dataIndex: 'value',
      key: 'value',
    },
  ];

  const getChartOptions = (data: number[], labels: string[], title: string) => ({
    chart: {
      type: 'pie',
      backgroundColor: 'transparent',
    },
    title: {
      text: title,
    },
    legend: {
      align: 'right',
      verticalAlign: 'middle',
      layout: 'vertical',
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
          format: '{point.name}: {point.percentage:.1f}%',
        },
        showInLegend: true,
      },
    },
    series: [
      {
        name: 'Share',
        colorByPoint: true,
        data: labels.map((label, index) => ({
          name: label,
          y: data[index],
        })),
      },
    ],
  });

  const preRfAeDataArray = [
    preRfAeData.normal || 0,
    preRfAeData.portscan || 0,
    preRfAeData.dos_slowloris || 0,
    preRfAeData.bruce_force || 0,
  ];
  const preRfAeLabels = ['Normal', 'Portscan', 'DoS Slowloris', 'Bruce Force'];

  const bertLabels = Object.keys(bertData);
  const bertDataArray = Object.values(bertData) as number[];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="container-wrapper">
      <Card className="card-container" size="small">
        <CardTitleCustom title="CHI TIẾT FLOW" />
        <Row gutter={[12, 12]}>
          {/* Bảng ở bên trái */}
          <Col span={10}>
            <div className="table-container">
              <SimpleTable
                columns={columns}
                dataSource={dataFlow}
              />
            </div>
          </Col>

          {/* Khoảng cách màu xám giữa 2 phần */}
          <Col span={1} className="spacing-between-columns" />

          {/* Phần chứa biểu đồ tròn ở bên phải */}
          <Col span={13}>
            <div className="right-side-container">
              <div className="threshold-container">
                <Text strong>Threshold: 0.03</Text>
                <br />
                <Text strong>MSE_Autoencoder: {preRfAeData.MSE_Autoencoder || 'N/A'}</Text>
              </div>
              <Button type="primary" onClick={handlePrint} className="print-button">
                Print
              </Button>
              <div className="pie-charts-container">
                {/* Biểu đồ tròn đầu tiên */}
                <div className="pie-chart">
                  <HighchartsReact
                    highcharts={Highcharts}
                    options={getChartOptions(preRfAeDataArray, preRfAeLabels, 'RandomForest')}
                  />
                </div>
                {/* Biểu đồ tròn thứ hai */}
                <div className="pie-chart">
                  <HighchartsReact
                    highcharts={Highcharts}
                    options={getChartOptions(bertDataArray, bertLabels, 'BERT')}
                  />
                </div>
              </div>
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default FlowDetails;
