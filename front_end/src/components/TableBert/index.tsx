import { Table } from "antd";
import React from "react";

interface TableBertProps {
  data: { [key: string]: string };
  customFields: { [key: string]: string };
}

// Định nghĩa kiểu cho dữ liệu nguồn
interface DataSourceType {
  key: number;
  field: string;
  value: string;
}

// Định nghĩa kiểu cho cột (không dùng ColumnType)
interface Column {
  title: string;
  dataIndex: string;
  key: string;
  align?: 'left' | 'right' | 'center'; // Kiểu của align phải là một trong các giá trị hợp lệ
}

const TableBert: React.FC<TableBertProps> = ({ data, customFields }) => {
  // Chuyển đổi dữ liệu thành định dạng phù hợp với bảng
  const dataSource: DataSourceType[] = Object.keys(customFields).map(
    (key, index) => ({
      key: index,
      field: customFields[key], // Hiển thị tên tùy chỉnh
      value: data[key],         // Giá trị tương ứng
    })
  );

  // Cấu hình cột của bảng theo cách thủ công
  const columns: Column[] = [
    {
      title: "Trường",
      dataIndex: "field",
      key: "field",
      align: "center", // Căn giữa tiêu đề cột
    },
    {
      title: "Giá trị",
      dataIndex: "value",
      key: "value",
      align: "center", // Căn giữa tiêu đề cột
    },
  ];

  return (
    <Table
      dataSource={dataSource}
      columns={columns}
      pagination={false}
      bordered
      size="middle"
    />
  );
};

export default TableBert;
