import { lazy } from "react";
import { FLOW_DETAILS } from "../../routes/route.constant";
const flowdetails = lazy(() => import("../FlowDetail"));

export default {
  path: FLOW_DETAILS ,
  element: flowdetails
};
