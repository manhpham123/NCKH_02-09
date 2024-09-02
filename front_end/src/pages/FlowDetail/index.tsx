import { Card, Tooltip, Typography } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../components/TableCustom";
import CardTitleCustom from "../../components/CardTitleCustom";
import { useParams } from 'react-router-dom';
const FlowDetails: FC = () => {
  const { id } = useParams();
  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Chi tiêt flow"/>
        {id}
      </Card>
    </div>
  );
};

export default FlowDetails;
