import { Card, Tooltip, Typography } from "antd";
import { FC, useState,useEffect } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../components/TableCustom";
import CardTitleCustom from "../../components/CardTitleCustom";
import { useParams } from 'react-router-dom';
import { FlowApi } from "../../apis/flow";
const FlowDetails: FC = () => {
  const [dataFlow, setDataFlow] = useState("");
  const { id } = useParams();

  const fetchDataFlow = async () => {

    const dataToSend = { 
      flow_id: id
  };
    const res = await FlowApi.GetFlowDetails(dataToSend);
    setDataFlow(res.data);
  }
  useEffect(() => {
    fetchDataFlow();
  }, [])

  return (
    <div className="container-wrapper">
      <Card className="card-container" size="small">
        <CardTitleCustom title="Chi tiêt flow"/>
        
      </Card>
    </div>
  );
};

export default FlowDetails;
