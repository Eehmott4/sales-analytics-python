import pandas as pd
import numpy as np

def calcular_faturamento(df: pd.DataFrame) -> float:
    return df["valor_total"].sum()


def calcular_ticket_medio(df: pd.DataFrame) -> float:
    faturamento_total = df["valor_total"].sum()
    total_vendas = df["id_venda"].nunique()
    return faturamento_total / total_vendas if total_vendas > 0 else 0


def top_produtos(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("produto")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


def faturamento_mensal(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()
    df_temp["mes"] = df_temp["data_venda"].dt.to_period("M").dt.to_timestamp()

    resultado = (
        df_temp.groupby("mes")["valor_total"]
        .sum()
        .reset_index()
    )

    return resultado


def frequencia_clientes(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("cliente_id")["id_venda"]
        .nunique()
        .reset_index(name="frequencia_compras")
    )


def curva_abc(df: pd.DataFrame) -> pd.DataFrame:
    vendas = (
        df.groupby("produto")["valor_total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    vendas["percentual"] = vendas["valor_total"] / vendas["valor_total"].sum()
    vendas["percentual_acumulado"] = vendas["percentual"].cumsum()

    def classificar(p):
        if p <= 0.8:
            return "A"
        elif p <= 0.95:
            return "B"
        else:
            return "C"

    vendas["classe"] = vendas["percentual_acumulado"].apply(classificar)

    return vendas
def rfm_analysis(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()

    df_temp["data_venda"] = pd.to_datetime(df_temp["data_venda"])

    snapshot_date = df_temp["data_venda"].max() + pd.Timedelta(days=1)

    rfm = df_temp.groupby("cliente_id").agg({
        "data_venda": lambda x: (snapshot_date - x.max()).days,
        "id_venda": "nunique",
        "valor_total": "sum"
    })

    rfm.columns = ["recencia", "frequencia", "monetario"]

    # Score de 1 a 5
    rfm["R_score"] = pd.qcut(rfm["recencia"], 5, labels=[5,4,3,2,1])
    rfm["F_score"] = pd.qcut(rfm["frequencia"].rank(method="first"), 5, labels=[1,2,3,4,5])
    rfm["M_score"] = pd.qcut(rfm["monetario"], 5, labels=[1,2,3,4,5])

    rfm["R_score"] = rfm["R_score"].astype(int)
    rfm["F_score"] = rfm["F_score"].astype(int)
    rfm["M_score"] = rfm["M_score"].astype(int)

    rfm["RFM_score"] = (
        rfm["R_score"].astype(str) +
        rfm["F_score"].astype(str) +
        rfm["M_score"].astype(str)
    )

    return rfm.reset_index()