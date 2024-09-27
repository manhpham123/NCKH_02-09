import {NCKHAxiosClient} from './base'

export const HostApi = {
    ToggleStatus: (id: number) => {
      return NCKHAxiosClient(`/toggle-status/${id}`, {
        method: "POST",
      });
    },
  };
  
