import React from 'react';
import { Table } from 'antd';
import { ColumnsType } from 'antd/es/table';

interface SimpleTableProps {
  columns: ColumnsType<any>;
  dataSource: any[];
}

const SimpleTable: React.FC<SimpleTableProps> = ({ columns, dataSource }) => {
  return (
    <Table columns={columns} dataSource={dataSource} pagination={false} />
  );
};

export default SimpleTable;
