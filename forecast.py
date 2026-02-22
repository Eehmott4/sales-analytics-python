import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


def preparar_serie_mensal(df: pd.DataFrame) -> pd.Series:
    df_temp = df.copy()
    df_temp["data_venda"] = pd.to_datetime(df_temp["data_venda"])
    df_temp.set_index("data_venda", inplace=True)

    serie_mensal = (
        df_temp["valor_total"]
        .resample("M")
        .sum()
    )

    return serie_mensal


def prever_vendas(df: pd.DataFrame, passos: int = 6):
    serie = preparar_serie_mensal(df)

    modelo = ARIMA(serie, order=(1, 1, 1))
    modelo_fit = modelo.fit()

    previsao = modelo_fit.forecast(steps=passos)

    return serie, previsao


def plot_previsao(serie_historica: pd.Series, previsao: pd.Series):
    plt.figure(figsize=(10, 5))

    plt.plot(serie_historica, label="Histórico")
    plt.plot(previsao, label="Previsão", linestyle="--")

    plt.title("Previsão de Vendas")
    plt.legend()
    plt.tight_layout()
    plt.show()