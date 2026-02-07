import React, { useState } from "react";
import { Button, Card, CardHeader, Table, Row } from "reactstrap";
import api from "../services/api";
import "./AnaliseEntryTable.css";

const linha_vazia = {
  cas: "",
  nome: "",
  efeito: "C",
  ambiente: "Aberto",
  vor: "",
  valor_vor: "",
  concentracao_max: "",
  solu_concentracao: 500,
};

const linha_vazia2 = {
  cas: "",
  nome: "",
  efeito: "NC",
  ambiente: "Aberto",
  vor: "",
  valor_vor: "",
  concentracao_max: "",
  solu_concentracao: 500,
};

const linha_vazia3 = {
  cas: "",
  nome: "",
  efeito: "C",
  ambiente: "Fechado",
  vor: "",
  valor_vor: "",
  concentracao_max: "",
  solu_concentracao: 500,
};

const linha_vazia4 = {
  cas: "",
  nome: "",
  efeito: "NC",
  ambiente: "Fechado",
  vor: "",
  valor_vor: "",
  concentracao_max: "",
  solu_concentracao: 500,
};

const AnaliseEntryTable = () => {
  // const das linhas da tabela
  const [rows, setRows] = useState([
    { ...linha_vazia },
    { ...linha_vazia2 },
    { ...linha_vazia3 },
    { ...linha_vazia4 },
  ]);

  const [loading, setLoading] = useState(false);

  // Função para adicionar uma nova linha vazia
  const handleAddRow = () => {
    setRows([...rows, { ...linha_vazia }]);
  };

  // Função para remover uma linha específica pelo index
  const handleRemoveRow = (index) => {
    const novasLinhas = [...rows];
    novasLinhas.splice(index, 1);
    setRows(novasLinhas);
  };

  // Função para atualizar o valor do campo quando digita
  const handleChange = (index, field, value) => {
    const novasLinhas = [...rows];
    novasLinhas[index][field] = value;
    setRows(novasLinhas);
  };

  // Salva no banco e depois baixa o Excel
  const handleSalvarEBaixar = async () => {
    setLoading(true);
    try {
      const responseSave = await api.post("/", rows);
      const dadosSalvos = responseSave.data;
      const ids = dadosSalvos.map((item) => item.id);

      if (!ids || ids.length === 0) {
        throw new Error("Nenhum ID retornado.");
      }
      const idsQuery = ids.join(",");
      const urlExcel = `exportar-excel/?ids=${idsQuery}`;

      // Faz a requisição do arquivo
      const responseExcel = await api.get(urlExcel, {
        responseType: "blob",
      });

      // Download
      const blobUrl = window.URL.createObjectURL(
        new Blob([responseExcel.data]),
      );
      const link = document.createElement("a");
      link.href = blobUrl;
      link.setAttribute("download", "Relatorio_Novos_Dados.xlsx");
      document.body.appendChild(link);
      link.click();

      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);

      alert("Sucesso! Dados salvos e relatório baixado.");
    } catch (error) {
      console.error(error);
      alert(
        "Erro ao processar. Verifique se os campos numéricos estão corretos.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Instruções */}
      <div
        className="bg-white rounded shadow py-3 px-4 mb-4 border-0"
        style={{ marginTop: "-12.2rem" }}
      >
        <Row>
          <div className="col-12">
            <h1 className="mb-0" style={{ color: "#e76a25", fontSize: "24px" }}>
              Avaliação de Risco
            </h1>
            <p
              className="mt-1 mb-0"
              style={{
                color: "#464646",
                fontSize: "14px",
                fontWeight: "bold",
              }}
            >
              Ferramenta para inserção, validação e geração automática de
              relatórios de conformidade ambiental.
            </p>
            <p
              className="mt-2 mb-0"
              style={{
                color: "#2b2b2b",
                fontSize: "14px",
                lineHeight: "1.5",
              }}
            >
              Preencha a tabela garantindo que cada contaminante possua
              registros para os cenários C e NC, bem como para ambientes Abertos
              e Fechados. <br></br> Ao final, clique no botão para salvar e
              gerar o relatório.
              <br />
              <br />
              <strong>Exemplos para Teste:</strong>
              <br />
              <span style={{ color: "#e65100" }}>
                • Para Laranja (Alerta):
              </span>{" "}
              Tente <strong>VOR = 100</strong> e <strong>Conc. Máx = 10</strong>{" "}
              (Valor menor que VOR).
              <br />
              <span style={{ color: "#607d8b" }}>
                • Para Cinza (Solubilidade):
              </span>{" "}
              Tente <strong>Conc. Máx = 600</strong> e{" "}
              <strong>Solubilidade = 500</strong> (Valor acima do limite).
            </p>
          </div>
        </Row>
      </div>

      {/* Tabela */}
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
                Entrada de Dados
              </h5>
            </div>
            <div className="col text-right">
              {/* Botão Único (Usa a classe verde do Excel) */}
              <Button
                className="btn-mini btn-excel"
                onClick={handleSalvarEBaixar}
                size="sm"
                disabled={loading}
                style={{
                  backgroundColor: "#28a745",
                  borderColor: "#28a745",
                  color: "#FFFFFF",
                  fontSize: "11px",
                  padding: "6px 12px",
                  fontWeight: "bold",
                }}
              >
                <i
                  className={`fas ${
                    loading ? "fa-spinner fa-spin" : "fa-save"
                  } mr-1`}
                />
                {loading ? "Processando..." : "Salvar e Baixar Relatório"}
              </Button>
            </div>
          </Row>
        </CardHeader>

        <div style={{ overflowX: "auto" }}>
          <Table
            className="align-items-center table-bordered mb-0"
            responsive
            style={{ margin: 0 }}
          >
            <thead>
              {/* Cabeçalho */}
              <tr>
                <th className="header-laranja" style={{ width: "10%" }}>
                  CAS Nº
                </th>
                <th className="header-laranja" style={{ width: "25%" }}>
                  CONTAMINANTE
                </th>
                <th className="header-laranja" style={{ width: "6%" }}>
                  EFEITO
                </th>
                <th className="header-laranja" style={{ width: "10%" }}>
                  AMBIENTE
                </th>
                <th className="header-laranja" style={{ width: "10%" }}>
                  FONTE VOR
                </th>
                <th className="header-laranja" style={{ width: "10%" }}>
                  VALOR VOR
                </th>
                <th className="header-laranja" style={{ width: "10%" }}>
                  CONC. MÁX
                </th>
                <th className="header-laranja" style={{ width: "10%" }}>
                  SOLUBILIDADE
                </th>
                <th className="header-laranja" style={{ width: "5%" }}>
                  #
                </th>
              </tr>
            </thead>
            {/* Inputs */}
            <tbody>
              {rows.map((row, index) => (
                <tr key={index}>
                  <td className="celula-input">
                    <input
                      className="input-tabela"
                      value={row.cas}
                      onChange={(e) =>
                        handleChange(index, "cas", e.target.value)
                      }
                      placeholder="00-00-0"
                    />
                  </td>
                  <td className="celula-input">
                    <input
                      className="input-tabela"
                      style={{ textAlign: "left" }}
                      value={row.nome}
                      onChange={(e) =>
                        handleChange(index, "nome", e.target.value)
                      }
                      placeholder="Nome..."
                    />
                  </td>
                  <td className="celula-input">
                    <select
                      className="select-tabela"
                      value={row.efeito}
                      onChange={(e) =>
                        handleChange(index, "efeito", e.target.value)
                      }
                    >
                      <option value="C">C</option>
                      <option value="NC">NC</option>
                    </select>
                  </td>
                  <td className="celula-input">
                    <select
                      className="select-tabela"
                      value={row.ambiente}
                      onChange={(e) =>
                        handleChange(index, "ambiente", e.target.value)
                      }
                    >
                      <option value="Aberto">Aberto</option>
                      <option value="Fechado">Fechado</option>
                    </select>
                  </td>
                  <td className="celula-input">
                    <input
                      className="input-tabela"
                      value={row.vor}
                      onChange={(e) =>
                        handleChange(index, "vor", e.target.value)
                      }
                    />
                  </td>
                  <td className="celula-input">
                    <input
                      type="number"
                      step="any"
                      className="input-tabela"
                      value={row.valor_vor}
                      onChange={(e) =>
                        handleChange(index, "valor_vor", e.target.value)
                      }
                    />
                  </td>
                  <td className="celula-input">
                    <input
                      type="number"
                      step="any"
                      className="input-tabela"
                      value={row.concentracao_max}
                      onChange={(e) =>
                        handleChange(index, "concentracao_max", e.target.value)
                      }
                    />
                  </td>
                  <td className="celula-input">
                    <input
                      type="number"
                      className="input-tabela"
                      value={row.solu_concentracao}
                      onChange={(e) =>
                        handleChange(index, "solu_concentracao", e.target.value)
                      }
                    />
                  </td>
                  <td className="celula-input text-center">
                    {rows.length > 1 && (
                      <Button
                        color="danger"
                        className="btn-mini"
                        onClick={() => handleRemoveRow(index)}
                        style={{
                          borderRadius: "50%",
                          width: "18px",
                          height: "18px",
                          padding: 0,
                          lineHeight: "18px",
                        }}
                      >
                        <i
                          className="fas fa-times"
                          style={{ fontSize: "9px" }}
                        />
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          {/* Botão de adicionar linha no final */}
          <div
            className="text-center p-2 border-top btn-add-row"
            onClick={handleAddRow}
          >
            <i className="fas fa-plus-circle mr-1"></i> ADICIONAR LINHA
          </div>
        </div>
      </Card>
    </>
  );
};

export default AnaliseEntryTable;
