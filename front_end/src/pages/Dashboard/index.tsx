import React, { useEffect, useState } from 'react';
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import './style.scss';
import { useDispatch } from "react-redux";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import { Card, Row, Col } from "antd";
import { ClusterOutlined, ShareAltOutlined, BugOutlined } from '@ant-design/icons';
import { useStaticService, useStaticProtocol, useStaticattack } from "../../utils/request/index";

type m = {
  "SSH"?: number;
  "Unknown"?: number;
  "FTP (Control)"?: number;
  "HTTP"?: number;
  "FTP (Data)"?: number;
  "HTTPS"?: number;
}

type attack = {
  "Bruce Force"?: number;
  "PortScan"?: number;
  "DoS slowloris"?: number;
  "Unknown attack"?: number;
  "BENIGN"?: number;
}

type ChartDataType = {
  name: string;
  y: number; // Assuming all values will be numbers
};

const Dashboard = () => {
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);  // Thêm trạng thái loading
  const [dataservice, setDataservice] = useState<m>({});
  const [chartData, setChartData] = useState<ChartDataType[]>([]);
  const [datatancong, setDatatancong] = useState<attack>({});
  
  const { data, mutate } = useStaticService(); 
  const { data: datagiaothuc } = useStaticProtocol();
  const { data: datapactack } = useStaticattack();
  
  const colors = ['#f64b71', '#f5820e', '#09dbd2', '#0fb7db', '#15c194', '#10906e', '#6377ff', '#5161d0'];

  useEffect(() => {
    let breadCrumb = [
      {
        label: "Dashboard",
        path: "",
      }
    ];
    dispatch(setSelectedBreadCrumb(breadCrumb));
  }, [dispatch]);

  useEffect(() => {
    if (data && datapactack) {
      const formattedData: ChartDataType[] = Object.entries(data).map(([key, value]) => ({
        name: key,
        y: value as number,  // Ensure that 'value' is treated as a number
      }));

      setChartData(formattedData);
      setDataservice(data);
      setDatatancong(datapactack);
      setLoading(false);  // Khi dữ liệu đã sẵn sàng, đặt loading thành false
    }
  }, [data, datapactack]);

  // Chuyển đổi dữ liệu từ backend thành mảng các cặp [key, value]
  const attackData: ChartDataType[] = Object.entries(datapactack || {}).map(([key, value]) => ({
    name: key,
    y: value as number,
  }));

  const topAttacks = attackData.slice(1, 4); // Lấy top 3 tấn công

  // Kiểm tra dữ liệu trước khi cấu hình biểu đồ
  const hasAttackData = datatancong && Object.keys(datatancong).length > 0;
  const hasProtocolData = datagiaothuc && Object.keys(datagiaothuc).length > 0;
  const hasServiceData = chartData && chartData.length > 0;

  // Cấu hình biểu đồ tấn công nếu có dữ liệu
  const tron_tan_cong = hasAttackData ? {
    chart: {
      type: 'pie',
      backgroundColor: 'white',
      height: 500,
      width: 690,
    },
    title: {
      text: 'THỐNG KÊ TẤN CÔNG'
    },
    plotOptions: {
      pie: {
        size: '100%',
        center: ['50%', '50%'],
        dataLabels: {
          enabled: false,
        },
        showInLegend: true
      }
    },
    legend: {
      align: 'right',
      layout: 'vertical',
      verticalAlign: 'middle',
      x: 0,
      itemStyle: {
        fontSize: '14px',
        color: '#333'
      },
      itemMarginBottom: 10,
      labelFormatter: function (this: Highcharts.Point): string {
        const name = this.name || '';
        let percentage = this.percentage !== undefined ? this.percentage.toFixed(1) : '0.0';
        percentage = isNaN(Number(percentage)) ? '0.0' : percentage;
        return `${name}: ${percentage} %`;
      }
    },
    series: [{
      name: 'số lượng flow',
      data: attackData,  // Sử dụng dữ liệu đã chuyển đổi từ backend
    }]
  } : null;

  // Cấu hình biểu đồ giao thức nếu có dữ liệu
  const tron_giao_thuc = hasProtocolData ? {
    chart: {
      type: 'pie',
      backgroundColor: 'white',
      height: 500,
      width: 690,
    },
    title: {
      text: 'THỐNG KÊ GIAO THỨC'
    },
    plotOptions: {
      pie: {
        size: '100%',
        center: ['50%', '50%'],
        dataLabels: {
          enabled: false,
        },
        showInLegend: true
      }
    },
    legend: {
      align: 'right',
      layout: 'vertical',
      verticalAlign: 'middle',
      x: 0,
      itemStyle: {
        fontSize: '14px',
        color: '#333'
      },
      itemMarginBottom: 10,
      labelFormatter: function (this: Highcharts.Point): string {
        const name = this.name || '';
        let percentage = this.percentage !== undefined ? this.percentage.toFixed(1) : '0.0';
        percentage = isNaN(Number(percentage)) ? '0.0' : percentage;
        return `${name}: ${percentage} %`;
      }
    },
    series: [{
      name: 'số lượng flow',
      data: Object.entries(datagiaothuc || {}).map(([key, value]) => ({
        name: key,
        y: value as number,
      })),
    }]
  } : null;

  // Cấu hình biểu đồ dịch vụ nếu có dữ liệu
  const BieuDoCot = hasServiceData ? {
    chart: {
      type: 'column',
      height: 500,
      backgroundColor: 'white',
    },
    title: {
      text: 'THỐNG KÊ DỊCH VỤ'
    },
    xAxis: {
      categories: chartData.map(item => item.name),
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Số lượng flow'
      }
    },
    series: [{
      name: 'Service',
      data: chartData.map((item, index) => ({
        y: item.y,
        color: colors[index % colors.length],
      })),
    }],
    plotOptions: {
      column: {
        colorByPoint: true,
        pointWidth: 130,
        borderRadius: 10,
        dataLabels: {
          enabled: true,
          style: {
            fontWeight: 'bold',
            fontSize: '13px',
          },
        },
      }
    }
  } : null;

  return (
    <div className="dashboard-wrapper">
      {loading ? (
        <p>Đang load dữ liệu...</p>  // Hiển thị thông báo khi đang tải dữ liệu
      ) : (
        <>
          {/*====================== Hàng đầu tiên: 4 khối thông tin thống kê ============*/}
          <Row gutter={[16, 16]} className="top-cards-row">
            <Col xs={24} sm={12} md={6}>
              <Card className="dashboard-card card-1">
                <div className="card-content">
                  <div className="card-info">
                    <h3 style={{ fontSize: '24px', fontWeight: '600', color: '#06275c', fontFamily: 'Arial, sans-serif', margin: 0 }}>Số File Độc Hại</h3>
                    <p style={{ fontSize: '24px', fontWeight: '600', color: '#06275c', fontFamily: 'Arial, sans-serif', margin: 0 }}>10</p>
                  </div>
                  <div className="card-icon">
                    <BugOutlined />
                  </div>
                </div>
              </Card>
            </Col>

            <Col xs={24} sm={12} md={6}>
              <Card className="dashboard-card card-2">
                <div className="card-content">
                  <div className="card-info">
                    <h3 style={{ fontSize: '24px', fontWeight: '600', color: '#8a433d', fontFamily: 'Arial, sans-serif', margin: 0 }}>Số Lượng Service</h3>
                    <p style={{ fontSize: '24px', fontWeight: '600', color: '#8a433d', fontFamily: 'Arial, sans-serif', margin: 0 }}>5</p>
                  </div>
                  <div className="card-icon">
                    <ClusterOutlined />
                  </div>
                </div>
              </Card>
            </Col>
            
<Col xs={24} sm={12} md={6}>
  <Card className="dashboard-card card-3" bodyStyle={{ padding: '0 0 20px 0' }}>
    <div style={{ textAlign: 'left', marginLeft: '20px' }}>  {/* Ghi đè thuộc tính căn giữa và thêm margin-left */}
      <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1b1529', marginBottom: '5px' ,marginLeft: '30px'}}>
        <ShareAltOutlined /> Top 3 Cuộc Tấn Công
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', paddingLeft: '20px', alignItems: 'flex-start', marginLeft: '20px' }}> {/* Sử dụng alignItems: 'flex-start' và thêm marginLeft */}
        {topAttacks.map((attack, index) => (
          <p key={attack.name} style={{ fontSize: '16px', fontWeight: '600', color: '#1b1529', fontFamily: 'Arial, sans-serif', margin: '0 0 0 20px' }}> {/* Thêm margin-left cho mỗi thẻ p */}
            {index + 1}. {attack.name}: {attack.y}
          </p>
        ))}
      </div>
    </div>
  </Card>
</Col>



            <Col xs={24} sm={12} md={6}>
              <Card className="dashboard-card card-4" bodyStyle={{ padding: '0 0 20px 0' }}>
                <div>
                  <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#ed0c31', marginBottom: '5px' }}>
                    <ShareAltOutlined /> Top 3 Rule
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>1. 2016672</p>
                    <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>2. 2017808</p>
                    <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>3. 2010963</p>
                  </div>
                </div>
              </Card>
            </Col>
          </Row>
          {/*======================== HẾT HÀNG THỨ NHẤT , 4 KHỐI THÔNG TIN THỐNG KÊ============= */}

          {/* =============Hàng thứ hai: 2 biểu đồ tròn theo chiều ngang: biểu đồ thống kê tấn công và giao thức */}
          <Row gutter={[30, 16]} className="chart-row">
            {tron_tan_cong ? (
              <Col xs={24} md={12}>
                <Card className="dashboard-card">
                  <HighchartsReact highcharts={Highcharts} options={tron_tan_cong} />
                </Card>
              </Col>
            ) : <p>Không có dữ liệu tấn công để hiển thị.</p>}
            
            {tron_giao_thuc ? (
              <Col xs={24} md={12}>
                <Card className="dashboard-card">
                  <HighchartsReact highcharts={Highcharts} options={tron_giao_thuc} />
                </Card>
              </Col>
            ) : <p>Không có dữ liệu giao thức để hiển thị.</p>}
          </Row>

          {/*=========== Hàng thứ ba: một biểu đồ cột thống kê các dịch vụ */}
          <Row gutter={[30, 16]} className="chart-row">
            {BieuDoCot ? (
              <Col xs={24} md={24}>
                <Card className="dashboard-card">
                  <HighchartsReact highcharts={Highcharts} options={BieuDoCot} />
                </Card>
              </Col>
            ) : <p>Không có dữ liệu dịch vụ để hiển thị.</p>}
          </Row>
          {/*======== Hết Hàng thứ ba */}
        </>
      )}
    </div>
  );
};

export default Dashboard;
