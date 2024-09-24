import { lazy } from "react";
import { ALERT_RULE   } from "../../routes/route.constant";
const rule_alert = lazy(() => import("../RuleAlert"));

export default {
  path: ALERT_RULE ,
  element: rule_alert,
};
