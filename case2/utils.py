import pandas as pd
import numpy as np
import io
import xlsxwriter

def processar_dataframe(file_obj):
    df = pd.read_excel(file_obj, sheet_name="Avaliacao_Risco_Case")
    df2 = pd.read_excel(file_obj, sheet_name="Valores_orientadores")

    # Limpeza de colunas/linhas
    df = df.drop(index=range(6))
    df = df.drop(columns=df.columns[0])

    # Renomear
    df = df.rename(
        columns={
            "Unnamed: 1": "CAS",
            "CONCENTRAÇÕES MÁXIMAS ACEITÁVEIS PARA ÁGUA SUBTERRÂNEA": "AMBIENTES ABERTOS",
            "Unnamed: 5": "AMBIENTES FECHADOS",
        }
    )

    # Preencher linhas
    fill = ["CAS", "CONTAMINANTE"]
    df[fill] = df[fill].ffill()

    # Unir tabelas
    df = df.merge(
        df2[["CAS", "VOR", "Valor VOR (mg/l)"]],
        left_on="CAS",
        right_on="CAS",
        how="left"
    )

    # Menor valor entre C e NC
    colunas_cnc = ["AMBIENTES ABERTOS", "AMBIENTES FECHADOS"]
    for col in colunas_cnc:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df["_temp_min_linha"] = df[colunas_cnc].min(axis=1)
    df["_temp_min_grupo"] = df.groupby("CAS")["_temp_min_linha"].transform("min")

    df["MENOR VALOR FINAL"] = np.where(
        df["_temp_min_grupo"] < df["Valor VOR (mg/l)"],
        df["Valor VOR (mg/l)"],
        df["_temp_min_grupo"]
    )

    df["MENOR VALOR FINAL"] = np.where(
        df["_temp_min_linha"].notna(), 
        df["MENOR VALOR FINAL"], 
        df["MENOR VALOR FINAL"] 
    )

    df["Concentração de solubilidade"] = 500

    # Comparação entre valores
    cols_comp = ["MENOR VALOR FINAL", "Valor VOR (mg/l)", "Concentração de solubilidade"]
    for col in cols_comp:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Cor Cinza - True se: Menor Valor > Solubilidade (500)
    df["Cinza"] = df["MENOR VALOR FINAL"] > df["Concentração de solubilidade"]

    # Cor Laranja - True se: Menor Valor < Valor VOR
    df["Laranja"] = df["_temp_min_grupo"] < df["Valor VOR (mg/l)"]

    # Limpeza das colunas temporárias
    df = df.drop(columns=["_temp_min_linha", "_temp_min_grupo"])

    # Remover NaN
    df = df.fillna("-")

    return df


def gerar_relatorio_excel(df):
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output, {"in_memory": True})
    ws = wb.add_worksheet("Relatório Consolidado")

    # Configuração de estilos base
    estilo_base = {
        "font_name": "Calibri",
        "font_size": 11,
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
    }
    
    estilo_topo = wb.add_format({**estilo_base, "bold": True, "bg_color": "#e76a25", "font_color": "#FFFFFF", "border": 1})
    estilo_colunas = wb.add_format({**estilo_base, "bold": True, "bottom": 2, "bottom_color": "#e76a25", "border": 1, "border_color": "#E8E8E8"})
    
    # Formatos de dados
    padrao = wb.add_format({**estilo_base, "border": 1, "border_color": "#E8E8E8"})
    numero = wb.add_format({**estilo_base, "border": 1, "border_color": "#E8E8E8", "num_format": "0.00E+00"})
    
    # Fundo Cinza
    estilo_cinza = wb.add_format({
        **estilo_base, 
        "bg_color": "#D3D3D3", 
        "bold": True, 
        "border": 1, 
        "border_color": "#E8E8E8",
        "num_format": "0.00E+00"
    })
    
    # Fonte Laranja
    estilo_coluna_vor_laranja = wb.add_format({
        **estilo_base, 
        "font_color": "#FF6600", 
        "bold": True, 
        "border": 1, 
        "border_color": "#E8E8E8",
        "num_format": "0.00"
    })

    # Cabeçalho
    ws.merge_range("G1:J2", "MÁXIMAS ACEITÁVEIS PARA ÁGUA\nNO PONTO DE EXPOSIÇÃO", estilo_topo)
    ws.merge_range("G3:J3", "VIA DE EXPOSIÇÃO: INALAÇÃO", estilo_topo)
    ws.merge_range("G4:H4", "AMBIENTE ABERTO", estilo_topo)
    ws.merge_range("I4:J4", "AMBIENTE FECHADO", estilo_topo)

    titulos = ["CAS", "CONTAMINANTE", "FONTE VOR", "VALOR VOR", "SOLUBILIDADE", "EFEITO"]
    for col, texto in enumerate(titulos):
        ws.merge_range(0, col, 4, col, texto, estilo_colunas)

    sub_titulos = ["CONC. MÁX\n(mg/L)", "VALOR CONSIDERADO\n(mg/L)", "CONC. MÁX\n(mg/L)", "VALOR CONSIDERADO\n(mg/L)"]
    for i, texto in enumerate(sub_titulos):
        ws.write(4, 6 + i, texto, estilo_colunas)

    # Prepara dados para agrupamento
    df_group = df.fillna("-")
    grupos = df_group.groupby(["CAS", "CONTAMINANTE", "VOR", "Valor VOR (mg/l)"], sort=False)

    linha = 5

    for (cas, nome, fonte_vor, valor_vor), grupo in grupos:
        n_linhas = len(grupo)
        linha_fim = linha + n_linhas - 1

        # Colunas fixas (mescladas)
        if n_linhas > 1:
            ws.merge_range(linha, 0, linha_fim, 0, cas, padrao)
            ws.merge_range(linha, 1, linha_fim, 1, nome, padrao)
            ws.merge_range(linha, 2, linha_fim, 2, fonte_vor, padrao)
        else:
            ws.write(linha, 0, cas, padrao)
            ws.write(linha, 1, nome, padrao)
            ws.write(linha, 2, fonte_vor, padrao)

        # Valor VOR com formatação laranja
        tem_alerta_laranja = grupo["Laranja"].any() if "Laranja" in grupo.columns else False
        estilo_atual_vor = estilo_coluna_vor_laranja if tem_alerta_laranja else padrao
        
        try:
            val_vor_num = float(valor_vor)
        except:
            val_vor_num = valor_vor

        if n_linhas > 1:
            ws.merge_range(linha, 3, linha_fim, 3, val_vor_num, estilo_atual_vor)
        else:
            ws.write(linha, 3, val_vor_num, estilo_atual_vor)

        # Solubilidade
        solubilidade = 500
        if n_linhas > 1:
            ws.merge_range(linha, 4, linha_fim, 4, solubilidade, padrao)
        else:
            ws.write(linha, 4, solubilidade, padrao)

        # Mescla Colunas Valor Considerado
        val_final = grupo.iloc[0]["MENOR VALOR FINAL"]
        if val_final == "-":
             validos = grupo[grupo["MENOR VALOR FINAL"] != "-"]["MENOR VALOR FINAL"]
             if not validos.empty:
                 val_final = validos.iloc[0]
        
        eh_cinza = grupo.iloc[0]["Cinza"] == True
        
        if eh_cinza:
            estilo_final = estilo_cinza
        else:
            estilo_final = numero

        if n_linhas > 1:
            ws.merge_range(linha, 7, linha_fim, 7, val_final, estilo_final)
        else:
            ws.write(linha, 7, val_final, estilo_final)

        if n_linhas > 1:
            ws.merge_range(linha, 9, linha_fim, 9, val_final, estilo_final)
        else:
            ws.write(linha, 9, val_final, estilo_final)

        # Linhas de detalhe
        for idx, row in grupo.iterrows():
            l_atual = linha + list(grupo.index).index(idx)
            
            # Coluna F: Efeito
            ws.write(l_atual, 5, row["EFEITO"], padrao)

            # Coluna G: Ambiente Aberto
            val_aberto = row["AMBIENTES ABERTOS"]
            ws.write(l_atual, 6, val_aberto if val_aberto != "-" else "-", numero if val_aberto != "-" else padrao)

            # Coluna I: Ambiente Fechado
            val_fechado = row["AMBIENTES FECHADOS"]
            ws.write(l_atual, 8, val_fechado if val_fechado != "-" else "-", numero if val_fechado != "-" else padrao)

        linha += n_linhas

    # Ajuste largura colunas
    larguras = [15, 30, 15, 12, 12, 8, 15, 15, 15, 15]
    for i, w in enumerate(larguras):
        ws.set_column(i, i, w)

    wb.close()
    output.seek(0)
    return output