import {NCKHAxiosClient} from './base'

export const FlowApi = {
  GetFlowDetails: (data: { flow_id?: string}) => {
    return NCKHAxiosClient("/flow-details/", {
        method: "GET",
        data: { // 2 thuộc tính content và file_name chính là 1 đối tượng mà backend yêu cầu
            flow_id: data.flow_id
        },
    });
},

};
