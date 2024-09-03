import { lazy } from "react";
import { CHECK_FILE  } from "../../routes/route.constant";
const check_file = lazy(() => import("../CheckFile"));

export default {
  path: CHECK_FILE,
  element: check_file,
};
