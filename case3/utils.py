import pandas as pd
import numpy as np

df = pd.read_excel("../data/Material_Case_Ex3.xlsx", sheet_name="EZMtp")
df2 = pd.read_excel("../data/Material_Case_Ex3.xlsx", sheet_name="Cadastro")

# Limpeza de colunas e cabeçalho
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

# Restruturar dados
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

# Mudar ordem das colunas
df = df[
    [
        "#sys_loc_code",
        "param_code",
        "param_value",
        "param_unit",
        "measurement_method",
        "measurement_date",
        "remark",
    ]
]

# Agrupar por
df = df.sort_values(by=["#sys_loc_code", "param_value"])

# Correção de nome linhas Cond
is_num = pd.to_numeric(df["param_value"], errors="coerce").notna()
cond = df["param_code"] == "Cond"
df.loc[cond, "param_code"] = np.where(
    is_num[cond], "Cond elet", "Cond clim"
)

# Limpeza de colunas e cabeçalho
df2 = df2.drop(columns=df2.columns[:2])
df2 = df2.drop(index=[0, 1, 3, 4, 5])

# Renomear
df2 = df2.rename(
    columns={
        'Unnamed: 2': "task_code",
    }
)

# Unir tabelas
df["task_code"] = df2["task_code"].iloc[0]

print(df.head(24))