import {NCKHAxiosClient} from './base'
import { FlowIdParams  } from "../constants/types/common.type";
export const FlowApi = {
    GetFlowDetails: (params: FlowIdParams )=>{
        return NCKHAxiosClient("/get_flow/",{
          method: "GET",
          params,
        })
      },
      GetBertPre: (params: FlowIdParams )=>{
        return NCKHAxiosClient("/get_bert_pre/",{
          method: "GET",
          params,
        })
      }
};
