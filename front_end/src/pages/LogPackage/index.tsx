import React, { useEffect } from 'react';

const Log_package = () => {
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => { // Chỉ định kiểu cho 'event'
      // Chỉ xử lý thông điệp từ dịch vụ con và kiểm tra nguồn gốc
      if (event.origin === "http://localhost:3001") {
        const { url } = event.data;
        if (url) {
          // Cập nhật URL của trình duyệt dịch vụ cha mà không tải lại trang
          window.history.pushState(null, '', new URL(url).pathname); 
        }
      }
    };

    window.addEventListener('message', handleMessage);

    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <div style={{ width: "100%" }}>
      <iframe
        src="http://localhost:3001/alerts#/alerts"
        width="100%"
        height="100%"
        frameBorder="0"
        title="Embedded Page"
      />
    </div>
  );
};

export default Log_package;
