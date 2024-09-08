import React, { FC, useEffect, useState } from "react";
import { Form, Space, message } from "antd";
import TextArea from "antd/es/input/TextArea";
import ButtonCustom from "../../components/ButtonCustom";
import { useParams } from 'react-router-dom';

import { RuleApi } from "../../apis/rule";

const RuleDetails: FC = () => {
  const [isEdit, setIsEdit] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [dataRule, setDataRule] = useState("");
  const [dataRuleChange, setDataRuleChange] = useState("");
  const { filename } = useParams();

  const handleCommandKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === '/' && e.ctrlKey) {
      e.preventDefault();
      const textArea = e.target as HTMLTextAreaElement;
      const selectionStart = textArea.selectionStart || 0;
      const selectionEnd = textArea.selectionEnd || 0;
      const startLineIndex = dataRuleChange.lastIndexOf('\n', selectionStart - 1) + 1;
      const endLineIndex = dataRuleChange.indexOf('\n', selectionEnd);
      const selectedLines = dataRuleChange.substring(startLineIndex, endLineIndex !== -1 ? endLineIndex : undefined);
      const modifiedLines = selectedLines.split('\n').map(line => {
        if (line.trim().startsWith('#')) return line.replace('#', '')
        else return '#' + line
      }).join('\n');
      const updateddataRuleChange = dataRuleChange.substring(0, startLineIndex) + modifiedLines + dataRuleChange.substring(endLineIndex !== -1 ? endLineIndex : dataRuleChange.length);
      setDataRuleChange(updateddataRuleChange);
    }
  }

  const fetchDataRule = async () => {
    setIsLoading(true);
    const res = await RuleApi.GetContentRule({ filename });
    setDataRule(res.data);
    setIsLoading(false);
  }

  useEffect(() => {
    if (dataRule) {
      setDataRuleChange(dataRule)
    }
  }, [dataRule]);

  useEffect(() => {
    fetchDataRule();
  }, []);

  const handleChangeRule = (e: any) => {
    setDataRuleChange(e.target.value);
  }

  const handleUpdate = async () => {
    const dataToSend = { 
      name: filename, 
      content_rule: dataRuleChange 
    };
    setIsLoading(true);
    const res = await RuleApi.updateRule(dataToSend);
    message.success('Cập nhật thành công');
    setIsLoading(false);
    fetchDataRule();
  }

  const handleCancel = () => {
    setIsEdit(false);
    setDataRuleChange(dataRule);
  }

  const handleFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();

      reader.onload = (event) => {
        const fileContent = event.target?.result as string;
        setDataRuleChange(fileContent);
      };

      // Đọc nội dung tệp dưới dạng văn bản (Text)
      reader.readAsText(file);
    }
  }

  return (
    <div className="container-wrapper">
      <Form>
        <TextArea rows={20} value={dataRuleChange} onChange={handleChangeRule} readOnly={!isEdit} onKeyUp={handleCommandKey} />
        <Space style={{ display: "flex", justifyContent: "end" }}>
          {isEdit ? (
            <>
              {/* Button Cancel */}
              <ButtonCustom
                size="small"
                onClick={handleCancel}
                label="Cancel"
                disabled={isLoading}
                style={{ margin: "10px 0" }}
              />
              
              {/* Button Save */}
              <ButtonCustom
                type="primary"
                size="small"
                onClick={handleUpdate}
                label="Save"
                loading={isLoading}
                style={{ margin: "10px 0" }}
              />

              {/* Button Import */}
              <ButtonCustom
                type="default"
                size="small"
                onClick={() => document.getElementById('file-input')?.click()}
                label="Import"
                style={{ margin: "10px 0" }}
              />
              <input
                type="file"
                accept=".txt,.json,.xml,.csv"  // Chấp nhận nhiều loại tệp
                style={{ display: "none" }}
                id="file-input"
                onChange={handleFileImport}
              />
            </>
          ) : (
            <ButtonCustom
              type="primary"
              size="small"
              onClick={() => setIsEdit(true)}
              label="Update"
              loading={isLoading}
              style={{ margin: "10px 0" }}
            />
          )}
        </Space>
      </Form>
    </div>
  );
};

export default RuleDetails;
