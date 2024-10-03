import { Button, Card, Tooltip, Typography, Modal } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";
import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";
import { useCheckFile } from "../../../utils/request";
import ListButtonActionUpdate from "../../../components/ListButtonActionUpdate";

const CheckFileTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  const {data, mutate,isLoading} = useCheckFile(params);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalContent, setModalContent] = useState<JSX.Element | null>(null);

  const showModal = (content: JSX.Element) => {
    setModalContent(content);
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  const getFileName = (filePath: string) => {
    return filePath.split('/').pop(); // Lấy tên file từ đường dẫn
  };
  const ChiTietFile = (_id: number) => {
    window.location.href = `http://localhost:3001/#/event/${_id}`;
};

 
  const columns: ColumnsType<any> = [
    {
      key: 1,
      title: "Số Thứ Tự",
      align: "center",
      width: "7%",
      render: (_, record, index) => {
        return index + 1;
      },
    },
    {
      key: 2,
      title: "Flow ID",
      dataIndex: "flow_id",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 3,
      title: "Thời Gian",
      dataIndex: "timestamp",
      align: "center",
      render: (timestamp) => (
        <Tooltip title={formatDate(timestamp)}>
          <div className="inline-text">{formatDate(timestamp)}</div>
        </Tooltip>
      ),
    },
    {
      key: 4,
      title: "Tên File",
      dataIndex: "filename",
      align: "center",
      render: (filename) => (
        <Tooltip title={getFileName(filename)}>
          <div className="inline-text">{getFileName(filename)}</div>
        </Tooltip>
      ),
    },
    
    {
      key: 5,
      title: "MD5",
      dataIndex: "md5",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    /*
    {
      key: 5,
      title: "SHA1",
      dataIndex: "sha1",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 6,
      title: "SHA256",
      dataIndex: "sha256",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    */
    {
      key: 6,
      title: "Source IP",
      dataIndex: "src_ip",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 7,
      title: "Source Port",
      dataIndex: "src_port",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 8,
      title: "Destination IP",
      dataIndex: "dest_ip",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 9,
      title: "Destination Port",
      dataIndex: "dest_port",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 10,
      title: "Chi Tiết Flow",
      align: "center",
      width: "8%",
      render: (_, record) => (
        <>
          <ListButtonActionUpdate
            // editFunction={() => {}}
            viewFunction={() =>  navigate(`/flow-details/${record.flow_id}`)}
          />
        </>
      ),
    },
    {
      key: 10,
      title: "Chi Tiết File",
      align: "center",
      width: "8%",
      render: (_, record) => (
        <>
        <ListButtonActionUpdate
          viewFunction={() => ChiTietFile(record._id)}
        />
      </>
      ),
    },
    // {
    //   key: 10,
    //   title: "Giao Thức",
    //   dataIndex: "protocol",
    //   align: "center",
    //   render: (group) => (
    //     <Tooltip title={group}>
    //       <div className="inline-text">{group}</div>
    //     </Tooltip>
    //   ),
    // },
    {
      key: 11,
      title: "Hành Động",
      align: "center",
      width: "10%",
      render: (_, record) => (
        <div>
          {/* <Button
            type="primary"
            style={{ marginRight: 8 }}
            onClick={() => handleCheckDb(record.md5)}
          >
            Check DB
          </Button> */}
          <Button
            type="primary"
            onClick={() => handleCheckFile(record.md5)}
          >
            Check File
          </Button>
        </div>
      ),
    }
  ];
 
const handleCheckFile = (md5: string) => {
  // navigate(`/file-details/${md5}`);
  window.open(`/file-details/${md5}`, '_blank');
  };

const handleCheckDb = (md5: string) => {
    alert(md5)
  
    //Dữ liệu mẫu trả về thành công
    // const response = {
    //   status: "success",
    //   name: "Trojan.Win32.Emotet.471040.A"
    // };

    const response = {
      status: "fail",
      name: "Không tìm thấy thông tin"
    };
    // Kiểm tra xem dữ liệu trả về có thành công không
    if (response.status === "success") {
      showModal(
        <div>
         <div>
          <Typography.Title level={3}>Kiểm Tra File Thành Công</Typography.Title>
         
            <strong style={{ fontWeight: "normal",fontSize: "18px" }} >Kết quả phát hiện:</strong>{" "}
            <span style={{ color: "red",fontSize: "18px" }}>{response.name}</span>
          
        </div>
        </div>
      );
    } else {
      showModal(
        <div>
        <Typography.Title level={3}>Kiểm Tra File Thất Bại</Typography.Title>
        <p style={{ fontWeight: "normal",fontSize: "18px" }}>Không tìm thấy thông tin file trong cơ sở dữ liệu.</p>
      </div>
      );
    }
  };
  

  const handleCheckVirusTotal = (md5: string) => {
    console.log("Check VirusTotal với mã MD5:", md5);
    showModal(
      <div>
      <Typography.Title level={4}>Check VirusTotal</Typography.Title>
      <p style={{ fontWeight: "normal" }}>MD5: {md5}</p>
      <p style={{ fontWeight: "normal" }}>Thêm nội dung modal ở đây...</p>
    </div>
    );
  };

  return (
    <div>
      <Card className="card-container" size="small">
        <CardTitleCustom title="Check File"/>
        <TableCustom
          dataSource={data?.data}
          columns={columns}
          bordered={true}
          isLoading={isLoading}
          limit={params.limit || 15 }
          total={data?.total}
          onLimitChange={(limit) => {
            setParams({ ...params, limit });
          }}
          onPageChange={(page) => {
            setParams({ ...params, page });
          }}
          page={params.page || 1}
        />
      </Card>
      <Modal
      title={<Typography.Title level={3}>Thông Tin Kiểm Tra File</Typography.Title>} // Tăng kích thước tiêu đề
      visible={isModalVisible}
      onOk={handleOk}
      onCancel={handleCancel}
      width={800} // Tăng kích thước modal
      style={{ borderRadius: "10px", overflow: "hidden" }} // Thêm phong cách cho modal
      bodyStyle={{ height: "200px", overflowY: "auto" }} // Tăng chiều cao của nội dung modal và cho phép cuộn
    >
      {modalContent}
      </Modal>
    </div>
  );
};

export default CheckFileTable;
