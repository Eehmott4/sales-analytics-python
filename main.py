from forecast import prever_vendas, plot_previsao
from data_loader import load_csv
from analysis import rfm_analysis
from analysis import (
    calcular_faturamento,
    calcular_ticket_medio,
    top_produtos,
    faturamento_mensal,
    frequencia_clientes,
    curva_abc
)
from visualization import (
    plot_faturamento_mensal,
    plot_top_produtos,
    plot_curva_abc,
    plot_frequencia_clientes
)


def main():
    df = load_csv("dados_vendas.csv")

    print("Faturamento Total:", calcular_faturamento(df))
    print("Ticket Médio:", calcular_ticket_medio(df))

    df_top = top_produtos(df)
    df_mensal = faturamento_mensal(df)
    df_freq = frequencia_clientes(df)
    df_abc = curva_abc(df)

    plot_faturamento_mensal(df_mensal)
    plot_top_produtos(df_top)
    plot_curva_abc(df_abc)
    plot_frequencia_clientes(df_freq)

    serie, previsao = prever_vendas(df)
    plot_previsao(serie, previsao)

    df_rfm = rfm_analysis(df)
    print("\nRFM Analysis:")
    print(df_rfm.head())

if __name__ == "__main__":
    main()
