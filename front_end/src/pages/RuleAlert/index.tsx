import React, { useEffect, useState } from "react";
import "./style.scss";
import RuleAlertTable from "./RuleAlertTable";
import { useDispatch } from "react-redux";
import { CHECK_FILE} from "../../routes/route.constant";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import RuleAlertFilter from "./RuleAlertFilter";

const RuleAlert = () => {
  const [filter, setFilter]= useState<any>({})
  const dispatch = useDispatch();
  useEffect(() => {
    let breadCrumb = [
       {
        label: "Rule-Alert",
        path: ""
       }
    ]
    dispatch(setSelectedBreadCrumb(breadCrumb))
  },[CHECK_FILE]) 
  return (
    <div className="container-wrapper">
      <div style={{marginBottom: "12px"}}>
        <RuleAlertFilter filters={filter} setFilters={setFilter}/>
      </div>
       <RuleAlertTable  />
    </div>
  );
};

export default RuleAlert;
