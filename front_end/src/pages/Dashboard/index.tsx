import React, { useEffect } from "react";
import DashboardChart from "./component/DashboardChart";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import './style.scss'
import { useDispatch } from "react-redux";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import DashboardGeneralItem from "./component/DashboardGeneralItem";
import { Space, message } from "antd";
import Icons from "../../assets/icons";
import DboardTopCardItem from "./component/DboardTopCardItem";
import { usePhantrang, useStaticService } from "../../utils/request";
import { Card, Row, Col } from "antd"; // Sử dụng các component từ Ant Design
import { UserOutlined, ShoppingCartOutlined, ProjectOutlined, ShareAltOutlined } from '@ant-design/icons'; // Import icons từ Ant Design


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
  
   // Cấu hình dữ liệu cho biểu đồ Highcharts
   const pieChartOptions1 = {
    chart: {
      type: 'pie'
    },
    title: {
      text: 'Biểu đồ tròn 1'
    },
    series: [{
      name: 'Số lượng',
      colorByPoint: true,
      data: [
        { name: 'Loại 1', y: 61.41 },
        { name: 'Loại 2', y: 11.84 },
        { name: 'Loại 3', y: 10.85 },
        { name: 'Loại 4', y: 4.67 },
      ]
    }]
  };

  const pieChartOptions2 = {
    chart: {
      type: 'pie'
    },
    title: {
      text: 'Biểu đồ tròn 2'
    },
    series: [{
      name: 'Số lượng',
      colorByPoint: true,
      data: [
        { name: 'Loại A', y: 45.41 },
        { name: 'Loại B', y: 21.84 },
        { name: 'Loại C', y: 18.85 },
        { name: 'Loại D', y: 7.67 },
      ]
    }]
  };

  return (
    <div className="dashboard-wrapper">
      {/* Hàng đầu tiên: 4 khối thông tin thống kê */}
      <Row gutter={[16, 16]} className="top-cards-row">
        <Col xs={24} sm={12} md={6}>
          <Card className="dashboard-card card-1" title={<><UserOutlined /> Khối 1</>}>
            <p>2,781</p>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="dashboard-card card-2" title={<><ShoppingCartOutlined /> Khối 2</>}>
            <p>3,241</p>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="dashboard-card card-3" title={<><ProjectOutlined /> Khối 3</>}>
            <p>253</p>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="dashboard-card card-4" title={<><ShareAltOutlined /> Khối 4</>}>
            <p>4,324</p>
          </Card>
        </Col>
      </Row>
 {/*======================== HẾT HÀNG THỨ NHẤT , 4 KHỐI THÔNG TIN THỐNG KÊ============= */}



      {/* Hàng thứ hai: 2 biểu đồ tròn theo chiều ngang */}
      <Row gutter={[16, 16]} className="chart-row">
        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={pieChartOptions1} />
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={pieChartOptions2} />
          </Card>
        </Col>
      </Row>
        {/*======== Hết Hàng thứ hai: 2 biểu đồ tròn theo chiều ngang================= */}


      {/* Hàng thứ ba: 2 biểu đồ tròn theo chiều ngang */}
      <Row gutter={[16, 16]} className="chart-row">
        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={pieChartOptions1} />
          </Card>
        </Col>
        <Col xs={24} md={12}>
          <Card className="dashboard-card">
            <HighchartsReact highcharts={Highcharts} options={pieChartOptions2} />
          </Card>
        </Col>
      </Row>
        {/*======== Hết Hàng thứ ba: 2 biểu đồ tròn theo chiều ngang================= */}

    </div>
  );
};

export default Dashboard;