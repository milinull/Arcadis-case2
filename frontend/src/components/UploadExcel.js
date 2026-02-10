import React, { useState, useRef } from "react";
import { Card, CardHeader, Row, Alert } from "reactstrap";
import axios from "axios";
import "./UploadExcel.css";

const UploadExcelComponent = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: null, msg: "" });
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.name.match(/\.(xlsx|xls)$/)) {
      setFile(selectedFile);
      setStatus({ type: null, msg: "" });
    } else {
      setStatus({ type: "danger", msg: "Apenas arquivos Excel (.xlsx, .xls)" });
    }
  };

  // Drag n Drop
  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDownloadExample = () => {
    // Link do Google Drive
    const driveLink =
      "https://docs.google.com/spreadsheets/d/1Niyi0FKPU_AO1-vQvRH_ht0bDwsjdqC6/export?format=xlsx";
    window.open(driveLink, "_blank");
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://35.175.150.159:8000/api/upload-excel/",
        formData,
        {
          responseType: "blob",
        },
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `processado_${file.name}`);
      document.body.appendChild(link);
      link.click();

      setStatus({ type: "success", msg: "Sucesso! Download iniciado." });
      setFile(null);
    } catch (err) {
      setStatus({ type: "danger", msg: "Erro no processamento." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Bloco de Instruções */}
      <div
        className="bg-white rounded shadow py-3 px-4 mb-4 border-0"
        style={{ marginTop: "-12.2rem" }}
      >
        <Row>
          <div className="col-12">
            <h1 className="mb-0" style={{ color: "#28a745", fontSize: "24px" }}>
              Conversão de Dados - Case 3
            </h1>
            <p
              className="mt-1 mb-0"
              style={{
                color: "#464646",
                fontSize: "14px",
                fontWeight: "bold",
              }}
            >
              Ferramenta para conversão automática de arquivos Excel para o
              padrão Arcadis.
            </p>
            <p
              className="mt-2 mb-0"
              style={{
                color: "#2b2b2b",
                fontSize: "14px",
                lineHeight: "1.5",
              }}
            >
              Faça upload do arquivo Excel bruto e o sistema irá processar
              automaticamente, convertendo os dados para o formato padronizado
              da Arcadis.
              <br />
              <br />
              <strong>Instruções:</strong>
              <br />
              <span style={{ color: "#28a745" }}>• Formatos aceitos:</span>{" "}
              Arquivos .xlsx e .xls
              <br />
              <span style={{ color: "#28a745" }}>• Processo:</span> Após o
              upload, o arquivo será processado e um novo arquivo Excel será
              gerado automaticamente para download.
              <br />
              <br />
              <strong>Teste com arquivo de exemplo:</strong>
              <br />
              <button
                onClick={handleDownloadExample}
                style={{
                  background: "none",
                  border: "none",
                  color: "#28a745",
                  textDecoration: "underline",
                  fontWeight: "bold",
                  cursor: "pointer",
                  padding: 0,
                  font: "inherit",
                }}
              >
                <i className="fas fa-download mr-1"></i>
                Baixar arquivo de exemplo (Case 3)
              </button>
            </p>
          </div>
        </Row>
      </div>

      {/* Card com Upload */}
      <Card
        className="mb-5"
        style={{
          boxShadow:
            "0 15px 35px rgba(50, 50, 93, 0.3), 0 5px 15px rgba(0, 0, 0, 0.2)",
        }}
      >
        <CardHeader className="border-0 py-2">
          <Row className="align-items-center">
            <div className="col">
              <h5
                className="mb-0 font-weight-bold text-uppercase text-muted"
                style={{ fontSize: "11px" }}
              >
                Upload de Arquivo
              </h5>
            </div>
          </Row>
        </CardHeader>

        <div className="p-4">
          {status.msg && <Alert color={status.type}>{status.msg}</Alert>}

          <div
            className={`upload-area ${file ? "has-file" : ""} ${isDragging ? "dragging" : ""}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => !file && fileInputRef.current.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              hidden
              onChange={(e) => handleFile(e.target.files[0])}
            />

            {!file ? (
              <div className="upload-content">
                <div className="upload-icon">
                  <i className="fas fa-cloud-upload-alt"></i>
                </div>
                <h3 className="upload-title">Arraste o arquivo aqui</h3>
                <p className="upload-subtitle">ou clique para selecionar</p>
                <p className="upload-formats">Formatos: .xlsx, .xls</p>
              </div>
            ) : (
              <div className="file-preview">
                <div className="file-icon">
                  <i className="fas fa-file-excel"></i>
                </div>
                <div className="file-info">
                  <p className="file-name">{file.name}</p>
                  <p className="file-size">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
                <button
                  className="btn-remove-file"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                  }}
                >
                  <i className="fas fa-times"></i>
                </button>
              </div>
            )}
          </div>

          {file && (
            <div className="text-center mt-4">
              <button
                className="btn-upload"
                onClick={handleUpload}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    Processando...
                  </>
                ) : (
                  <>
                    <i className="fas fa-check mr-2"></i>
                    Confirmar Processamento
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </Card>
    </>
  );
};

export default UploadExcelComponent;
