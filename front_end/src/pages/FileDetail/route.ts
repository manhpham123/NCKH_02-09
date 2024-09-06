import { lazy } from "react";
import { FILE_DETAILS } from "../../routes/route.constant";
const filedetails = lazy(() => import("../FileDetail"));

export default {
  path: FILE_DETAILS  ,
  element: filedetails
};
