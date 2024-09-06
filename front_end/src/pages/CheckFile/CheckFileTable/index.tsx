import { Button, Card, Tooltip, Typography, Modal } from "antd";
import { FC, useState } from "react";
import { ColumnsType } from "antd/es/table";

import "./style.scss";
import TableCustom from "../../../components/TableCustom";
import { CommonGetAllParams } from "../../../constants/types/common.type";
import CardTitleCustom from "../../../components/CardTitleCustom";
import { useNavigate } from "react-router-dom";

const CheckFileTable: FC = () => {
  const navigate = useNavigate();
  const [params, setParams] = useState<CommonGetAllParams>({
    limit: 10,
    page: 1,
  });
  //const {data, mutate,isLoading} = useCheckFile(params);
  const isLoading = false;
  const data = {
    "data": [
      {
        "filename": "example1.exe",
        "md5": "f46bad29a32c8f0b27de63af58f76118",
        "sha1": "ee9051de481b6eb24bc625c2028f79b947035495",
        "sha256": "0e37b1329d6b6544ef24d204f4146f1445b5cdc33c46447de8e6c2c525f1fd6a",
        "size":76
      },
      {
        "filename": "example2.exe",
        "md5": "f0942ad9e7216ade8fd1118d33ec6151",
        "sha1": "90d805f00a2c27ca97dfdbd8965f082a6cd06af4",
        "sha256": "0da8a8a5eadc4fcb63a1ac452d084a8166882b3a9dbe202c574c632a194e50b2",
        "size":84
      },
      {
        "filename": "demo1.txt",
        "md5": "aa46425b529620edf837ea951cc28dcc",
        "sha1": "f0cf7442560e1c76ce61365a8b2f1f9dbb90dcd7",
        "sha256": "490d00c18b3bbfde087655b955c3ac3a32d36ec5fb8ce2d485ecd34ccce4d1db",
        "size":121
      },
      {
        "filename": "ddos.exe",
        "md5": "1217746c141eec70a23f191cfbcaff8d",
        "sha1": "26ddf97b32709c4ee87cf7248e906e24c6a68e77",
        "sha256": "bfb8861c57f4bb54628020ff0e95f7d000579f8c3a323bd1d3e6e4a872f3d245",
        "size":50
      },
      {
        "filename": "portscan.exe",
        "md5": "4d0bd356ea616ffa0687437edd9771da",
        "sha1": "30875ab155cde70844208e3af1cc6db16458e4b4",
        "sha256": "dcee09f8a5fe56552dd43d2400990ab65fde4821b78c87748417f8d5b904889f",
        "size":300
      },
      {
        "filename": "example3.exe",
        "md5": "5780e00e9cc633815e46f76ccb662cbe",
        "sha1": "da2e35e0e5ee30efbb51e95afa2be326e0211b18",
        "sha256": "2aec68c3818dc471865d8ca5f88d783943c1efff0f66360736a09026565035b4",
        "size":101
      },
      {
        "filename": "example4.txt",
        "md5": "7277b2e269528fb20d6d2681be354b93",
        "sha1": "7b4fc67e2938ae5c707162e2f06521bfc1719b23",
        "sha256": "cada223faa617fb038a5d6040d6bbe318a8d6a455377fbc5362ad82f0b741e2e",
        "size":120
      },
      {
        "filename": "demo2.exe",
        "md5": "1ffdb66e829387a9d10032af888e9639",
        "sha1": "06a5b4e196a197e5fce24fd07d374b5f0841ce2a",
        "sha256": "4931e5d3811a460f47678631f4bdc82c9c6e9176ae3940403e690bc82e3714a9",
        "size":374
      },
      {
        "filename": "demo3.txt",
        "md5": "0da9851aec9b55401560a80652ef22a6",
        "sha1": "f4614e579ae7977d467dd23fdadd4184f729f671",
        "sha256": "0fd55b4277f417ddcf927bc94bff8b96415b9630dfcf3e8aac3e153dc015a4a9",
        "size":225
      },
      {
        "filename": "example5.txt",
        "md5": "99847fa8352b1477dbf752ee33ecea14",
        "sha1": "23a857a56d8cad76a3be365e144f179cfc6088ed",
        "sha256": "28cf97f72cdba738fe94806e047be6ed4b261c1ef1eceec6f4f30a511d914aa7",
        "size":200
      }
    ],
    "limit": 10,
    "page": 1,
    "total": 100
  }
  
  // const [isEditSystemParamsModalShow, SetIsEditSystemParamsModalShow] =
  //   useState(false);
  // const [selectedRule, setSelectedRule] = useState<any>({});
  // const closeEditSystemParamsModal = () => {
  //   SetIsEditSystemParamsModalShow(false);
  // };
  // const openEditSystemParamsModal = (record: any) => {
  //   SetIsEditSystemParamsModalShow(true);
  //   setSelectedRule(record);
  // };
 
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
 
  const columns: ColumnsType<any> = [
    {
      key: 1,
      title: "Số Thứ Tự",
      align: "center",
      width: "10%",
      render: (_, record, index) => {
        return index + 1;
      },
    },
    {
      key: 2,
      title: "Tên File",
      dataIndex: "filename",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 3,
      title: "MD5",
      dataIndex: "md5",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 4,
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
      key: 5,
      title: "SHA256",
      dataIndex: "sha256",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 6,
      title: "Kích Thước (KB)",
      dataIndex: "size",
      align: "center",
      render: (group) => (
        <Tooltip title={group}>
          <div className="inline-text">{group}</div>
        </Tooltip>
      ),
    },
    {
      key: 7,
      title: "Hành Động",
      align: "center",
      width: "20%",
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
  navigate(`/file-details/${md5}`);
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
