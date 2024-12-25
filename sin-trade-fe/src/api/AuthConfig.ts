export interface DataResponse {
    status: string;
    data: string;
  }
  

export const dataUrl: string = import.meta.env.VITE_BACKEND_URL as string;
