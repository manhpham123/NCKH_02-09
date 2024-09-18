import React, { useEffect, useState } from 'react';
import DashboardChart from "./component/DashboardChart";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import './style.scss'
import { useDispatch } from "react-redux";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import { Card, Row, Col } from "antd"; // Sử dụng các component từ Ant Design
import { ClusterOutlined, ProjectOutlined, ShareAltOutlined,BugOutlined } from '@ant-design/icons'; // Import icons từ Ant Design
import {useStaticService,useStaticProtocol,useStaticattack } from "../../utils/request/index";
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
"BENIGN"?:number;
}
type ChartDataType = {
  name: string;
  y: number; // Assuming all values will be numbers
};

const Dashboard = () => {
  const dispatch = useDispatch();
  useEffect(() => {
    let breadCrumb = [
      {
        label: "Dashboard",
        path: "",
      }
    ]
    dispatch(setSelectedBreadCrumb(breadCrumb))
  }, [])
  const [dataservice,setDataservice] = useState<m>({});
  const {data,mutate} =  useStaticService(); 
  const [chartData, setChartData] = useState<ChartDataType[]>([]); // Specify the type here
  const {data:datagiaothuc} =  useStaticProtocol();
  const [datatancong,setDatatancong] = useState<attack>({});
  const {data:datapactack} =  useStaticattack();
  const colors = ['#f64b71','#f5820e','#09dbd2','#0fb7db','#15c194','#10906e','#6377ff','#5161d0'];
  useEffect(() => {
    if(data && datapactack){
      const formattedData: ChartDataType[] = Object.entries(data).map(([key, value]) => ({
        name: key,
        y: value as number,  // Ensure that 'value' is treated as a number
      }));
  
        setChartData(formattedData)
        setDataservice(data)
        setDatatancong(datapactack)
    }
},[])

const topAttacks = Object.entries(datapactack).slice(0, 3);
//============== Cấu hình biểu đồ tròn, thống kê các cuộc tấn công
const tron_tan_cong = {
  chart: {
    type: 'pie',
    backgroundColor: 'white', // Màu nền cho biểu đồ
    height: 500,  // Tăng chiều cao của biểu đồ
    width: 690,   // Tăng chiều rộng của biểu đồ
  
  },
  title: {
    text: 'Thống kê tấn công'
  },
  plotOptions: {
    pie: {
      size: '100%', // Giảm kích thước của biểu đồ tròn xuống 60% để có không gian cho chú thích
      center: ['50%', '50%'], // Căn chỉnh biểu đồ tròn sang bên trái
      dataLabels: {
        enabled: false, // Tắt hiển thị các nhãn dữ liệu trên biểu đồ
      },
      showInLegend: true // Hiển thị các mục trong chú thích (legend)
    }
  },
  legend: {
    align: 'right',  // Căn chỉnh chú thích về phía bên phải
    layout: 'vertical',  // Đặt chú thích theo chiều dọc
    verticalAlign: 'middle',  // Căn giữa chú thích theo chiều dọc
    x: 0, // Tạo khoảng cách giữa chú thích và biểu đồ
    itemStyle: {
      fontSize: '14px', // Đặt kích thước font chữ của chú thích
      color: '#333'  // Đặt màu chữ cho chú thích
    },
    itemMarginBottom: 10,  // Điều chỉnh khoảng cách giữa các hàng của chú thích
    labelFormatter: function (this: Highcharts.Point): string {  // Định nghĩa kiểu 'this' là Highcharts.Point
      const name = this.name || '';  // Kiểm tra 'name' không bị undefined
      let percentage = this.percentage !== undefined ? this.percentage.toFixed(1) : '0.0'; // Kiểm tra 'percentage' không bị undefined
      percentage = isNaN(Number(percentage)) ? '0.0' : percentage; // Kiểm tra nếu 'percentage' là NaN, thì đặt thành '0.0'
      return `${name}: ${percentage} %`;  // Trả về chuỗi định dạng
    }
  },
  series: [{
    name: 'số lượng flow',
    data: [
      { name: 'Port Scan', y: datatancong?.PortScan, color: '#02b2af' },
      { name: 'Unknown attack', y: datatancong?.['Unknown attack'], color: '#2e96ff' },
      { name: 'DoS', y: datatancong['DoS slowloris'], color: '#b800d8' },
      { name: 'Bruce Force', y: datatancong['Bruce Force'], color: '#2731c8' },
      { name: 'BENIGN', y: datatancong.BENIGN, color: '#60009b' }
    ]
  }]
};
//========================================================================
 //============== Cấu hình biểu đồ tròn, thống kê các giao thức
const tron_giao_thuc = {
  chart: {
    type: 'pie',
    backgroundColor: 'white', // Màu nền cho biểu đồ
    height: 500,  // Tăng chiều cao của biểu đồ
    width: 690,   // Tăng chiều rộng của biểu đồ
  
  },
  title: {
    text: 'Thống kê Protocol'
  },
  plotOptions: {
    pie: {
      size: '100%', // Giảm kích thước của biểu đồ tròn xuống 60% để có không gian cho chú thích
      center: ['50%', '50%'], // Căn chỉnh biểu đồ tròn sang bên trái
      dataLabels: {
        enabled: false, // Tắt hiển thị các nhãn dữ liệu trên biểu đồ
      },
      showInLegend: true // Hiển thị các mục trong chú thích (legend)
    }
  },
  legend: {
    align: 'right',  // Căn chỉnh chú thích về phía bên phải
    layout: 'vertical',  // Đặt chú thích theo chiều dọc
    verticalAlign: 'middle',  // Căn giữa chú thích theo chiều dọc
    x: 0, // Tạo khoảng cách giữa chú thích và biểu đồ
    itemStyle: {
      fontSize: '14px', // Đặt kích thước font chữ của chú thích
      color: '#333'  // Đặt màu chữ cho chú thích
    },
    itemMarginBottom: 10,  // Điều chỉnh khoảng cách giữa các hàng của chú thích
    labelFormatter: function (this: Highcharts.Point): string {  // Định nghĩa kiểu 'this' là Highcharts.Point
      const name = this.name || '';  // Kiểm tra 'name' không bị undefined
      let percentage = this.percentage !== undefined ? this.percentage.toFixed(1) : '0.0'; // Kiểm tra 'percentage' không bị undefined
      percentage = isNaN(Number(percentage)) ? '0.0' : percentage; // Kiểm tra nếu 'percentage' là NaN, thì đặt thành '0.0'
      return `${name}: ${percentage} %`;  // Trả về chuỗi định dạng
    }
  },
  series: [{
    name: 'số lượng flow',
    data: [
      { name: 'TCP', y: datagiaothuc?.TCP, color: '#02b2af' },
      { name: 'UDP', y: datagiaothuc?.UDP, color: '#2e96ff' }
    ]
  }]
};
//========================================================================
const optionsCot = {
  chart: {
    type: 'column',
    height: 500,  
    backgroundColor: 'white', // Màu nền cho biểu đồ
  },
  title: {
    text: 'Thống Kê Service'
  },
  xAxis: {
    categories: chartData.map(item => item.name), // Lấy tên của các service cho trục X
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
      color: colors[index % colors.length], // Đặt màu cho mỗi cột theo thứ tự trong mảng mã màu
    })),
  }],
  plotOptions: {
    column: {
      colorByPoint: true, // Cho phép mỗi cột có màu riêng biệt
      pointWidth: 130, // Đặt chiều rộng cột nhỏ hơn
      borderRadius: 10, // Bo tròn các góc của cột
      dataLabels: {
        enabled: true, // Hiển thị giá trị trên đầu mỗi cột
        style: {
          fontWeight: 'bold',
          fontSize: '13px',
        },
      },
    }
  }
};
  return (
    <div className="dashboard-wrapper">

      {/*====================== Hàng đầu tiên: 4 khối thông tin thống kê ============*/}
      <Row gutter={[16, 16]} className="top-cards-row">
      <Col xs={24} sm={12} md={6}>
    <Card className="dashboard-card card-1">
      <div className="card-content">
        <div className="card-info">
          <h3 style={{ fontSize: '24px', fontWeight: '600', color: '#06275c', fontFamily: 'Arial, sans-serif', margin: 0 }}>Số File Độc Hại</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: '#06275c', fontFamily: 'Arial, sans-serif', margin: 0 }}>10</p>
          {/* <div className="card-sub-info">
            <span className="card-change">
              <ArrowUpOutlined /> 8.2% last week
            </span>
          </div> */}
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
          {/* <div className="card-sub-info">
            <span className="card-change">
              <ArrowUpOutlined /> 5.1% last week
            </span>
          </div> */}
        </div>
        <div className="card-icon">
          <ClusterOutlined />
        </div>
      </div>
    </Card>
  </Col>
  <Col xs={24} sm={12} md={6}>
  <Card className="dashboard-card card-3" bodyStyle={{ padding: '0 0 20px 0' }}>
    <div>
      <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#1b1529', marginBottom: '5px' }}>
        <ShareAltOutlined /> Top 3 Cuộc Tấn Công
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {topAttacks.map(([attackType, count], index) => (
          <p key={attackType} style={{ fontSize: '16px', fontWeight: '600', color: '#1b1529', fontFamily: 'Arial, sans-serif', margin: 0  }}>
            {index + 1}. {attackType}: {count as number}
          </p>
        ))}
      </div>
    </div>
  </Card>
</Col>

<Col xs={24} sm={12} md={6}>
  <Card className="dashboard-card card-4" bodyStyle={{ padding:'0 0 20px 0' }}>
    <div>
      <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#ed0c31', marginBottom: '5px' }}>
        <ShareAltOutlined /> Top 3 Rule
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}> {/* Sử dụng Flexbox cho bố cục dọc */}
        <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>1. 12345</p>
        <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>2. 56789</p>
        <p style={{ fontSize: '16px', fontWeight: '600', color: '#ed0c31', fontFamily: 'Arial, sans-serif', margin: 0 }}>3. 13271</p>
      </div>
    </div>
  </Card>
</Col>

      </Row>
 {/*======================== HẾT HÀNG THỨ NHẤT , 4 KHỐI THÔNG TIN THỐNG KÊ============= */}


      {/* =============Hàng thứ hai: 2 biểu đồ tròn theo chiều ngang: biểu đồ thống kê tấn công và giao thức */}
      <Row gutter={[30, 16]} className="chart-row">

        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={tron_tan_cong} />
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={tron_giao_thuc} />
          </Card>
        </Col>
      </Row>
        {/*======== Hết Hàng thứ hai: 2 biểu đồ tròn theo chiều ngang================= */}


      {/*=========== Hàng thứ ba: một biểu đồ cột thống kê các dịch vụ */}
      <Row gutter={[30, 16]} className="chart-row">
        <Col xs={24} md={24}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={optionsCot} />
          </Card>
        </Col>
      </Row>
        {/*======== Hết Hàng thứ ba */}

    </div>
  );
};

export default Dashboard;