import { NCKHAxiosClient } from './base';
import { Md5Params } from "../constants/types/common.type";

export const FileApi = {
  GetFileDetails: (params: Md5Params) => {
    const { md5 } = params; // Lấy giá trị md5 từ tham số
    return NCKHAxiosClient(`/search/${md5}`, {  // Đưa md5 trực tiếp vào URL
      method: "GET"
    });
  }
};
