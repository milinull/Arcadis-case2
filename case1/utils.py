import camelot
import pandas as pd
import numpy as np
import io

def processar_dataframe(file_obj):
    tables = camelot.read_pdf(file_obj, pages='1', flavor='stream')
    tables2 = camelot.read_pdf(file_obj, pages='1', flavor='stream')

    # Transforma em DataFrame
    df = tables[0].df
    df2 = tables2[0].df

    # Limpeza de colunas/linhas e cabeçalho
    df = df.drop(index=range(13))
    header = df.iloc[0].fillna('') + " " + df.iloc[1].fillna('')
    df.columns = [h.strip() for h in header]
    df = df.iloc[2:].reset_index(drop=True)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.dropna(axis=1, how='all')
    df = df.drop(columns=df.columns[5:])

    # Renomear
    df = df.rename(
        columns={
            "": "Diluição",
        }
    )

    # Trocar células que começam com < por LQ
    df = df.replace(r'^\s*<\s*[\d,.]+\s*$', '< LQ', regex=True)

    # Limpeza de colunas/linhas e cabeçalho
    df2 = df2.drop(index=range(7))
    df2 = df2.iloc[0:4]

    # Juntar dados
    df2[1] = (
        df2[1].fillna("").astype(str).str.strip() + "" + df2[2].fillna("").astype(str).str.strip()
    ).str.strip()

    df2 = df2.drop(columns=df2.columns[2:])

    # Transformação coluna/linha
    df2 = df2.set_index(0).T

    # Correção caracteres da coluna
    df2.columns = df2.columns.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    df2["Data da Amostragem :"] = pd.to_datetime(
        df2['Data da Amostragem :'], 
        dayfirst=True, 
        errors='coerce'
    )

    # Unir tabelas
    df = df.merge(df2, how='cross')

    # Renomear
    df = df.rename(
        columns={
            "Amostra Rotulada como:": "Nome da amostra",
            "Parâmetros": "Parâmetro químico",
            "Resultados analíticos": "Resultados",
            "Data da Amostragem :": "Data"
        }
    )

    # data excel
    data_excel = pd.Timestamp('1899-12-30')

    df["Identificação interna"] = (
        df["Nome da amostra"].astype(str).str.strip() + "_" +
        (df["Data"] - data_excel).dt.days.astype(str)
    )

    # Criar as colunas finais de visualização
    df["Data de coleta"] = df["Data"].dt.strftime('%d/%m/%Y')
    df["Horário de coleta"] = df["Data"].dt.time

    # Converter unidades
    if "Unidade" in df.columns:
        df["Unidade"] = df["Unidade"].astype(str).str.replace('µ', 'u').str.replace('μ', 'u')

    # Mudar ordem das colunas
    df = df[
        [
            "Identificação interna",
            "Nome da amostra",
            "Data de coleta",
            "Horário de coleta",
            "Parâmetro químico",
            "Resultados",
            "Unidade",
        ]
    ]
    
    df["Limite de Quantificação (LQ)"] = 500

    return df


def gerar_excel_formatado(df):
    output = io.BytesIO()

    # Criação arquivo Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')

        workbook = writer.book
        worksheet = writer.sheets['Dados']

        # Formato para < LQ (Fundo Cinza, Texto)
        formato_cinza = workbook.add_format({
            'bg_color': '#D3D3D3',
            'border': 1,
            'align': 'center'
        })

        # Formato para números em negrito
        formato_numero_float = workbook.add_format({
            'bold': True,
            'border': 1,
            'num_format': '0.00', 
            'align': 'center'
        })
        
        formato_texto_padrao = workbook.add_format({
            'border': 1,
            'align': 'center'
        })

        # Tenta localizar a coluna "Resultados"
        try:
            col_idx = df.columns.get_loc("Resultados")
        except KeyError:
            return output

        # Itera sobre as linhas
        for row_idx, valor in enumerate(df["Resultados"]):
            excel_row = row_idx + 1
            valor_str = str(valor).strip()

            # É < LQ
            if "< LQ" in valor_str.upper():
                worksheet.write(excel_row, col_idx, valor_str, formato_cinza)
            
            # É Número
            else:
                try:
                    # Trocar vírgula por ponto
                    valor_limpo = valor_str.replace(',', '.')
                    
                    # Converter para FLOAT nativo do Python
                    valor_float = float(valor_limpo)
                    
                    # Usar write_number
                    worksheet.write_number(excel_row, col_idx, valor_float, formato_numero_float)
                
                except ValueError:
                    # Se falhar a conversão, escreve como texto normal
                    worksheet.write(excel_row, col_idx, valor_str, formato_texto_padrao)

        # Ajuste de largura das colunas
        for i, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(i, i, max_len)

    output.seek(0)
    return output