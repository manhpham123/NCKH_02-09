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

    const res = await FlowApi.GetFlowDetails({flow_id: id });
    //console.log(res.data.info)
    //console.log(res.data.pre_rf_ae)
    console.log(res.data.bert)
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
