import {NCKHAxiosClient} from './base'
import { Md5Params   } from "../constants/types/common.type";
export const FileApi = {
    GetFileDetails: (params: Md5Params  )=>{
        return NCKHAxiosClient("/.../",{
          method: "GET",
          params,
        })
      }
};
