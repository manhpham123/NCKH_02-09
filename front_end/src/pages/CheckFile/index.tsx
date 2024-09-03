import React, { useEffect, useState } from "react";
import "./style.scss";
import CheckFileTable from "./CheckFileTable";
import { useDispatch } from "react-redux";
import { CHECK_FILE} from "../../routes/route.constant";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import CheckFileFilter from "./CheckFileFilter";

const CheckFile = () => {
  const [filter, setFilter]= useState<any>({})
  const dispatch = useDispatch();
  useEffect(() => {
    let breadCrumb = [
       {
        label: "CheckFile",
        path: ""
       }
    ]
    dispatch(setSelectedBreadCrumb(breadCrumb))
  },[CHECK_FILE]) 
  return (
    <div className="container-wrapper">
      <div style={{marginBottom: "12px"}}>
        <CheckFileFilter filters={filter} setFilters={setFilter}/>
      </div>
       <CheckFileTable  />
    </div>
  );
};

export default CheckFile;
