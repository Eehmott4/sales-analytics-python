import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_faturamento_mensal(df_mensal: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_mensal, x="mes", y="valor_total")
    plt.title("Faturamento Mensal")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_top_produtos(df_top: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_top, x="produto", y="quantidade")
    plt.title("Top Produtos Mais Vendidos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_curva_abc(df_abc: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_abc, x=range(len(df_abc)), y="percentual_acumulado")
    plt.axhline(0.8, linestyle="--")
    plt.axhline(0.95, linestyle="--")
    plt.title("Curva ABC")
    plt.tight_layout()
    plt.show()


def plot_frequencia_clientes(df_freq: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    sns.histplot(df_freq["frequencia_compras"], bins=20)
    plt.title("Distribuição da Frequência de Compras")
    plt.tight_layout()
    plt.show()