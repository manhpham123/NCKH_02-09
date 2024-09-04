import { FC, useState } from "react";
import "./style.scss";
import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import { useNavigate } from "react-router-dom";
import { Card } from "antd";
import { useMonitorFlow } from "../../utils/request/index";

const MonitorFlow: FC = () => {
  const navigate = useNavigate();
  const [selectedPoint, setSelectedPoint] = useState(null);
   const {data:flow_data} =  useMonitorFlow();

  // const flow_data = {
  //   "data": [
  //     { "flow_id": "fl00001", "dos_slowloris": 10, "portscan": 30, "bruce_force": 20, "normal": 40, "time": "2024-08-29 21:00:00" },
  //     { "flow_id": "fl00002", "dos_slowloris": 10, "portscan": 30, "bruce_force": 20, "normal": 40, "time": "2024-08-29 22:00:00" },
  //     { "flow_id": "fl00003", "dos_slowloris": 40, "portscan": 20, "bruce_force": 10, "normal": 30, "time": "2024-08-29 23:00:00" },
  //     // Các đối tượng khác...
  //   ]
  // };

  // Hàm chuyển đổi flow_id thành dạng số
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
        radius: 4
      }
    },
    {
      name: 'Port_Scan',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.portscan, flow_id: item.flow_id })),
      color: '#ff7f0e',
      marker: {
        symbol: 'circle',
        fillColor: '#ff7f0e',
        radius: 4
      }
    },
    {
      name: 'Bruce_Force',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.bruce_force, flow_id: item.flow_id })),
      color: '#2ca02c',
      marker: {
        symbol: 'circle',
        fillColor: '#2ca02c',
        radius: 4
      }
    },
    {
      name: 'Normal',
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.normal, flow_id: item.flow_id })),
      color: '#9467bd',
      marker: {
        symbol: 'circle',
        fillColor: '#9467bd',
        radius: 4
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
      }
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
      data: flow_data?.data.map((item: any) => ({ x: parseFlowId(item.flow_id), y: item.MSE_Autoencoder, flow_id: item.flow_id })),
      color: '#1f77b4',
      marker: {
        symbol: 'circle',
        fillColor: '#1f77b4',
        radius: 4
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
      }
    },
    yAxis: {
      title: {
        text: 'Ngưỡng'
      },
      tickInterval: 0.005,
      labels: {
        formatter: function (this: Highcharts.AxisLabelsFormatterContextObject) {
          return `${this.value}`;
        }
      },
      min: 0,
      max: 0.05
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
              //alert(`Flow ID: ${point.flow_id}`);
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

  </div>
  );
};

export default MonitorFlow;