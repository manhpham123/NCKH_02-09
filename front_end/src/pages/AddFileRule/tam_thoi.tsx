import React, { useEffect, useState } from "react";
import "./style.scss";
import { useDispatch } from "react-redux";
import { RULE_MANAGEMENT } from "../../routes/route.constant";
import { setSelectedBreadCrumb } from "../App/store/appSlice";
import { Form, Input, Space, Typography, message } from "antd";
import ButtonCustom from "../../components/ButtonCustom";
import { useForm } from "antd/es/form/Form";
import TextArea from "antd/es/input/TextArea";
import { RuleApi } from "../../apis/rule";

const AddFileRule = () => {
  const dispatch = useDispatch();
  const [dataRuleFileChange, setDataRuleFileChange] = useState("");
  const [form] = useForm();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let breadCrumb = [
      {
        label: "Rule Management",
        path: RULE_MANAGEMENT,
      },
      {
        label: "Create File Config",
        path: "",
      },
    ];
    dispatch(setSelectedBreadCrumb(breadCrumb));
  }, [dispatch]); // Sửa RULE_MANAGEMENT thành dispatch

  const handleCommandKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "/" && e.ctrlKey) {
      e.preventDefault();
      const textArea = e.target as HTMLTextAreaElement;
      const selectionStart = textArea.selectionStart || 0;
      const selectionEnd = textArea.selectionEnd || 0;
      const startLineIndex =
        dataRuleFileChange.lastIndexOf("\n", selectionStart - 1) + 1;
      const endLineIndex = dataRuleFileChange.indexOf("\n", selectionEnd);

      const selectedLines = dataRuleFileChange.substring(
        startLineIndex,
        endLineIndex !== -1 ? endLineIndex : undefined
      );

      const modifiedLines = selectedLines
        .split("\n")
        .map((line) => {
          if (line.trim().startsWith("#")) return line.replace("#", "");
          else return "#" + line;
        })
        .join("\n");
      const updateddataRuleFileChange =
        dataRuleFileChange.substring(0, startLineIndex) +
        modifiedLines +
        dataRuleFileChange.substring(
          endLineIndex !== -1 ? endLineIndex : dataRuleFileChange.length
        );
      setDataRuleFileChange(updateddataRuleFileChange);
    }
  };

  const handleChangeRuleFile = (e: any) => {
    setDataRuleFileChange(e.target.value);
  };

  const createRuleFileHanlder = async (values: any) => {
    const filenameWithExtension = `${values.name}.rules`;
    const dataToSend = {
      name: filenameWithExtension,
      content_rule: values.rules,
    };
    setIsLoading(true);
    try {
      const res = await RuleApi.addRuleFile(dataToSend);
      if (res.status === 200) {
        message.success("Tạo File Thành Công");
        form.resetFields();
        setDataRuleFileChange(""); // Xóa dữ liệu sau khi tạo file thành công
      } else message.error("Tạo File Thất Bại");
    } catch (error) {
      message.error("Tạo File Thất Bại");
    }
    setIsLoading(false);
  };

  const handleImportFile = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const fileContent = e.target?.result;
        if (typeof fileContent === "string") {
          setDataRuleFileChange(fileContent); // Cập nhật nội dung vào state
          form.setFieldsValue({ rules: fileContent }); // Cập nhật nội dung vào form
        }
      };
      reader.readAsText(file);
    }
  };

  return (
    <div className="container-wrapper">
      <Typography
        className="addFileRule-title"
        style={{ marginBottom: "10px", fontSize: "1.5rem" }}
      >
        Tạo Mới File Rule
      </Typography>
      <Form
        form={form}
        layout="vertical"
        className="add-fileRule-form"
        onFinish={createRuleFileHanlder}
      >
        <Form.Item
          label="Tên File"
          name="name"
          rules={[{ required: true }]}
        >
          <Input placeholder="Rule" addonAfter=".rules" />
        </Form.Item>
        <Form.Item
          label="Nội Dung"
          name="rules"
          rules={[{ required: true }]}
        >
          <TextArea
            rows={18}
            value={dataRuleFileChange}
            onChange={handleChangeRuleFile}
            onKeyUp={handleCommandKey}
          />
        </Form.Item>
        <Space style={{ justifyContent: "end", width: "100%" }}>
          <ButtonCustom
            label="Tạo File"
            bgColor="#2862AF"
            type="primary"
            htmlType="submit"
            onClick={() => {}}
            loading={isLoading}
          />
          {/* Nút Import */}
          <ButtonCustom
            label="Import"
            bgColor="#2862AF"
            type="default"
            onClick={() => document.getElementById("fileInput")?.click()}
          />
          <input
            type="file"
            id="fileInput"
            style={{ display: "none" }}
            accept=".txt,.json,.xml,.csv, .rules"  // Chấp nhận nhiều loại tệp
            onChange={handleImportFile}
          />
        </Space>
      </Form>
    </div>
  );
};

export default AddFileRule;
