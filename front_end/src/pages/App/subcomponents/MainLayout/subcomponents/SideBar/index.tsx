import React from "react";
import { Menu, Row, Space, Typography } from "antd";
import type { MenuProps } from "antd";
import { ApartmentOutlined, AppstoreFilled,PieChartOutlined,ClusterOutlined,BranchesOutlined,BellOutlined,SettingOutlined,
  ControlOutlined, AuditOutlined,UnorderedListOutlined ,NodeIndexOutlined, FileOutlined 
  } from "@ant-design/icons";
import {
  CUSTOMER,
  ACCOUNT,
  SETTING,
  DASHBOARD,
  LOG,
  LOG_PACKAGE,
  FLOW_MANAGEMENT,
  AGENT_MANAGEMENT,
  ALERT,
  RULE_MANAGEMENT,
  MONITOR_FLOW,
  CHECK_FILE,
  ALERT_RULE
} from "../../../../../../routes/route.constant";
import { Link } from "react-router-dom";

import "./style.scss";
import { useDispatch } from "react-redux";
import { changeActiveTab } from "../../../../store/appSlice";


type MenuItem = Required<MenuProps>['items'][number];
function getItem(
  label: React.ReactNode,
  key?: React.Key | null,
  icon?: React.ReactNode,
  children?: MenuItem[],
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem(<Link to={DASHBOARD}>THỐNG KÊ</Link>, '1', <PieChartOutlined />,),
  getItem(<Link to={FLOW_MANAGEMENT}>QUẢN LÝ FLOW</Link>, '2', <BranchesOutlined  />),
  getItem(<Link to={AGENT_MANAGEMENT}>QUẢN LÝ MÁY</Link>, '3', <AppstoreFilled />),
  getItem(<Link to={ALERT}>QUẢN LÝ THÔNG BÁO</Link>, '4', <BellOutlined  />),
  // getItem( <Link to={RULE}>Rule</Link>,'5', <AppstoreFilled />,
  //   getItem( <Link to={RULE}>Rule</Link>, '3', <AppstoreFilled />),
  // // getItem(<Link to={}>Thông Báo</Link>, '4', <AppstoreFilled />),
  // ) 

  getItem('QUẢN LÝ RULE BASE', '5', <ControlOutlined />, [
    getItem(<Link to={LOG_PACKAGE}>DANH SÁCH SỰ KIỆN</Link>, '5-1', <UnorderedListOutlined />),
    getItem(<Link to={ALERT_RULE}>DANH SÁCH ALERT</Link>, '5-2', <BellOutlined />),
    getItem(<Link to={RULE_MANAGEMENT}>QUẢN LÝ RULE</Link>, '5-3', <SettingOutlined />)
    // getItem(<Link to={`${RULE}/2`}>MannagerRule</Link>, '5-2', <AppstoreFilled />),
  ]),
  getItem(<Link to={MONITOR_FLOW}>THEO DÕI FLOW</Link>, '6', <AppstoreFilled />),
  getItem(<Link to={CHECK_FILE}>QUẢN LÝ FILE</Link>, '7', <FileOutlined  />)
];

/*
const items: MenuItem[] = [
  getItem(<Link to={DASHBOARD}>Thống Kê</Link>, '1', <PieChartOutlined />,),
  getItem(<Link to={FLOW_MANAGEMENT}>Quản Lý Flow</Link>, '2', <BranchesOutlined  />),
 // getItem(<Link to={AGENT_MANAGEMENT}>Quản Lý Máy</Link>, '3', <AppstoreFilled />),
  getItem(<Link to={ALERT}>Thông Báo</Link>, '4', <BellOutlined  />),
  // getItem( <Link to={RULE}>Rule</Link>,'5', <AppstoreFilled />,
  //   getItem( <Link to={RULE}>Rule</Link>, '3', <AppstoreFilled />),
  // // getItem(<Link to={}>Thông Báo</Link>, '4', <AppstoreFilled />),
  // ) 

  getItem('Rule Base', '5', <ControlOutlined />, [
    getItem(<Link to={LOG_PACKAGE}>Log</Link>, '5-1', <UnorderedListOutlined />),
    getItem(<Link to={RULE_MANAGEMENT}>RULE</Link>, '5-2', <SettingOutlined />)
    // getItem(<Link to={`${RULE}/2`}>MannagerRule</Link>, '5-2', <AppstoreFilled />),
  ]),
  getItem(<Link to={MONITOR_FLOW}>FLOW</Link>, '6', <AppstoreFilled />),
  getItem(<Link to={CHECK_FILE}>FILE</Link>, '7', <FileOutlined  />)
];
*/


export const SideBar: React.FC = () => {
  return (
    <div className="sideBar-container">
      <Space direction="vertical" size={20}>
        <Row className="w-100 menuTab">
          <Menu
            defaultSelectedKeys={['1']}
            defaultOpenKeys={['sub1']}
            inlineIndent={10}
            items={items}
            mode="inline"
          />
        </Row>
      </Space>
    </div >
  );
};
