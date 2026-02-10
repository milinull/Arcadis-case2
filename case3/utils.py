import pandas as pd
import numpy as np
import io


def processar_dataframe(file_obj):
    df = pd.read_excel(file_obj, sheet_name="EZMtp")
    df2 = pd.read_excel(file_obj, sheet_name="Cadastro")

    # Limpeza de colunas/linhas e cabeçalho
    df = df.drop(columns=df.columns[:3])
    df = df.drop(index=[1, 2])
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # Renomear
    df = df.rename(
        columns={
            'measurement_date ("DD/MM/AA HH:MM")': "measurement_date",
            np.nan: "time",
        }
    )

    # Juntar data + hora
    df["measurement_date"] = pd.to_datetime(df["measurement_date"]) + pd.to_timedelta(
        df["time"].astype(str)
    )
    df = df.drop(columns=df.columns[2])

    # Reestruturar dados
    df = df.melt(
        id_vars=[
            "#sys_loc_code",
            "measurement_date",
            "measurement_method",
            "remark",
        ],
        var_name="param_code",
        value_name="param_value",
    )

    # Dividir valores
    df[["param_code", "param_unit"]] = (
        df["param_code"].str.strip().str.extract(r"^([A-Za-zÀ-ÿ\s]+?)(?:\s+([^\d]+))?$")
    )

    # Remover parenteses e o que estiver fora
    df["param_unit"] = (
        df["param_unit"]
        .str.extract(r"\((.*?)\)", expand=False)
        .fillna(df["param_unit"])
        .str.strip()
    )

    df = df.rename(columns={"#sys_loc_code": "sys_loc_code"})

    # Mudar ordem das colunas
    df = df[
        [
            "sys_loc_code",
            "param_code",
            "param_value",
            "param_unit",
            "measurement_method",
            "measurement_date",
            "remark",
        ]
    ]

    # Agrupar por
    df = df.sort_values(by=["sys_loc_code", "param_value"])

    # Correção de nome linhas Cond
    is_num = pd.to_numeric(df["param_value"], errors="coerce").notna()
    cond = df["param_code"] == "Cond"
    df.loc[cond, "param_code"] = np.where(is_num[cond], "Cond elet", "Cond clim")

    # Limpeza de colunas/linhas e cabeçalho
    df2 = df2.drop(columns=df2.columns[:2])
    df2 = df2.drop(index=[0, 1, 3, 4, 5])

    # Renomear
    df2 = df2.rename(
        columns={
            "Unnamed: 2": "task_code",
        }
    )

    # Unir tabelas
    df["task_code"] = df2["task_code"].iloc[0]

    return df


def gerar_excel_formatado(df):
    """Gera o Excel formatado baseado no DataFrame processado"""
    output = io.BytesIO()

    # Criação arquivo Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados Processados')

        worksheet = writer.sheets['Dados Processados']

        # Ajuste de largura das colunas
        for i, col in enumerate(df.columns):
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(i, i, max_len)

    output.seek(0)
    return output