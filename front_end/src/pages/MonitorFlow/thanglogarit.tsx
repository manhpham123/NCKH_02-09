import { FC, useState } from "react";
import "./style.scss";
import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import { useNavigate } from "react-router-dom";
import { Card } from "antd";
import { useMonitorFlow } from "../../utils/request/index";
import FlowManagement from "../FlowManagement"; // Nhập thành phần FlowManagement

const MonitorFlow: FC = () => {
  const navigate = useNavigate();
  const [selectedPoint, setSelectedPoint] = useState(null);
   const {data:flow_data} =  useMonitorFlow();

  const parseFlowId = (flow_id: string): number => {
    return parseInt(flow_id.replace('fl', ''), 10);  // Loại bỏ 'fl' và chuyển sang số
  };  

  const seriesDataMot: any[] = [
    {
      name: 'Dos_Slowloris',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.dos_slowloris, flow_id: item.flow_id })),
      color: '#1f77b4',
      marker: {
        symbol: 'circle',
        fillColor: '#1f77b4',
        radius: 4,
        enabled: false 
      }
    },
    {
      name: 'Port_Scan',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.portscan, flow_id: item.flow_id })),
      color: '#ff7f0e',
      marker: {
        symbol: 'circle',
        fillColor: '#ff7f0e',
        radius: 4,
        enabled: false 
      }
    },
    {
      name: 'Bruce_Force',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.bruce_force, flow_id: item.flow_id })),
      color: '#2ca02c',
      marker: {
        symbol: 'circle',
        fillColor: '#2ca02c',
        radius: 4,
        enabled: false 
      }
    },
    {
      name: 'Normal',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.normal, flow_id: item.flow_id })),
      color: '#9467bd',
      marker: {
        symbol: 'circle',
        fillColor: '#9467bd',
        radius: 4,
        enabled: false 
      }
    }
  ];

  const options_mot: Highcharts.Options = {
    chart: {
      type: 'line',
      height: 400,
      scrollablePlotArea: {
        minWidth: 30000,
      }
    },
    title: {
      text: 'RandomForest'
    },
    xAxis: {
      type: 'linear',
      title: {
        text: 'Flow'
      },
      min: 0,  // Thiết lập giá trị nhỏ nhất của trục X là 0
      max: flow_data && flow_data.data.length > 0 ? parseFlowId(flow_data.data[0].flow_id)+1: undefined, 
      crosshair: {
        color: '#ff0000',
        width: 2,
        dashStyle: 'ShortDash'
      },
      scrollbar: {
        enabled: true,
        barBackgroundColor: '#888888',
        barBorderRadius: 7,
        barBorderWidth: 0,
        buttonBackgroundColor: '#cccccc',
        buttonBorderWidth: 0,
        rifleColor: '#000000',
        trackBackgroundColor: '#eeeeee',
        trackBorderWidth: 1
      },
      reversed: true, // Đảo ngược trục X để hiển thị theo thứ tự giảm dần
    },
    yAxis: {
      title: {
        text: 'Dự Đoán'
      },
      tickInterval: 20,
      labels: {
        formatter: function (this: Highcharts.AxisLabelsFormatterContextObject) {
          return `${this.value} %`;
        }
      },
      min: 0,
      max: 105
    },
    tooltip: {
      shared: true,
      formatter: function (this: Highcharts.TooltipFormatterContextObject) {
        const pointsFormatted = this.points?.map(point => {
          return `${point.series.name}: ${point.y} %`;
        }).join('<br/>');
        return `<b>${this.x}</b><br/>${pointsFormatted}`;
      }
    },
    series: seriesDataMot,
    plotOptions: {
      series: {
        point: {
          events: {
            click: function () {
              const point = this as any;
              //alert(`Flow ID: ${point.flow_id}`);
              setSelectedPoint(point);
              navigate(`/flow-details/${point.flow_id}`);
            }
          }
        }
      }
    }
  };
  const seriesDataHai: any[] = [
    {
      name: 'MSE Autoencoder',
      data: flow_data?.data.map((item: any) => ({
        x: parseFlowId(item.flow_id),
        y: item.MSE_Autoencoder,
        flow_id: item.flow_id
      })),
      color: '#1f77b4',
      marker: {
        symbol: 'circle',
        fillColor: '#1f77b4',
        radius: 4,
        enabled: false
      }
    }
  ];

  const options_hai: Highcharts.Options = {
    chart: {
      type: 'line',
      height: 400,
      scrollablePlotArea: {
        minWidth: 30000,
      }
    },
    title: {
      text: 'Auto Encoder'
    },
    xAxis: {
      type: 'linear',
      title: {
        text: 'Flow'
      },
      min: 0, // Thiết lập giá trị nhỏ nhất của trục X là 0
      max: flow_data && flow_data.data.length > 0 ? parseFlowId(flow_data.data[0].flow_id) + 1 : undefined,
      crosshair: {
        color: '#ff0000',
        width: 2,
        dashStyle: 'ShortDash'
      },
      scrollbar: {
        enabled: true,
        barBackgroundColor: '#888888',
        barBorderRadius: 7,
        barBorderWidth: 0,
        buttonBackgroundColor: '#cccccc',
        buttonBorderWidth: 0,
        rifleColor: '#000000',
        trackBackgroundColor: '#eeeeee',
        trackBorderWidth: 1
      },
      reversed: true, // Đảo ngược trục X để hiển thị theo thứ tự giảm dần
    },
    yAxis: {
      title: {
        text: 'Ngưỡng'
      },
      type: 'logarithmic', // Sử dụng thang đo logarit để hiển thị các giá trị chênh lệch lớn
      minorTickInterval: 0.1, // Hiển thị các tick nhỏ hơn
      labels: {
        formatter: function (this: Highcharts.AxisLabelsFormatterContextObject) {
          return `${this.value}`;
        }
      },
      min: Math.max(Math.min(...flow_data?.data.map((item: any) => item.MSE_Autoencoder)), 1e-5), // Đảm bảo giá trị min > 0 cho trục logarit
      max: Math.max(...flow_data?.data.map((item: any) => item.MSE_Autoencoder)) * 1.1, // Điều chỉnh giá trị max một chút để có khoảng không gian
      plotLines: [{
        color: 'red', // Màu của đường ngang
        value: 0.0035, // Giá trị trên trục y mà đường sẽ vẽ
        width: 2, // Độ dày của đường
        label: {
          text: 'Ngưỡng 0.0035', // Văn bản hiển thị trên đường
          align: 'right', // Vị trí của văn bản (left, center, right)
          style: {
            color: 'red',
            fontWeight: 'bold'
          }
        }
      }]
    },
    tooltip: {
      shared: true,
      formatter: function (this: Highcharts.TooltipFormatterContextObject) {
        const pointsFormatted = this.points?.map(point => {
          return `${point.series.name}: ${point.y} `;
        }).join('<br/>');
        return `<b>${this.x}</b><br/>${pointsFormatted}`;
      }
    },
    series: seriesDataHai,
    plotOptions: {
      series: {
        point: {
          events: {
            click: function () {
              const point = this as any;
              setSelectedPoint(point);
              navigate(`/flow-details/${point.flow_id}`);
            }
          }
        }
      }
    }
  };
 

  return (
    <div className ="container" style={{ width: '100%' }} >
            {/* Hiển thị thành phần FlowManagement ở đây
            <FlowManagement /> */}
  
    <Card className="card-container" size="small">

    <div className="highcharts-container">
    <HighchartsReact
      highcharts={Highcharts}
      options={options_mot}
    />
  </div>
    </Card>

  <Card className="card-container" size="small">
<div className="highcharts-container">
<HighchartsReact
  highcharts={Highcharts}
  options={options_hai}
/>
</div>
</Card>
         {/* Hiển thị thành phần FlowManagement ở đây */}
         <FlowManagement />
  </div>
  );
};

export default MonitorFlow;