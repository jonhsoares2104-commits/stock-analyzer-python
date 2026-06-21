import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from rich import print
import os


os.makedirs("graficos", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)


def analisar_acao(ticker):

    print(f"\n[cyan]Buscando {ticker}...[/cyan]")

    acao = yf.Ticker(ticker)

    dados = acao.history(period="6mo")

    if dados.empty:
        print("[red]Ação não encontrada[/red]")
        return

    dados["MM20"] = dados["Close"].rolling(20).mean()
    dados["MM50"] = dados["Close"].rolling(50).mean()

    delta = dados["Close"].diff()

    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)

    rs = ganho.rolling(14).mean() / perda.rolling(14).mean()

    dados["RSI"] = 100 - (100 / (1 + rs))

    preco = dados["Close"].iloc[-1]
    mm20 = dados["MM20"].iloc[-1]
    mm50 = dados["MM50"].iloc[-1]
    rsi = dados["RSI"].iloc[-1]

    info = acao.info

    print("\n[bold green]===== ANÁLISE =====[/bold green]")

    print("Empresa:", info.get("longName"))
    print("Setor:", info.get("sector"))

    print(f"Preço: R$ {preco:.2f}")
    print(f"MM20: R$ {mm20:.2f}")
    print(f"MM50: R$ {mm50:.2f}")
    print(f"RSI: {rsi:.2f}")

    if mm20 > mm50:
        print("[green]Tendência: ALTA 📈[/green]")
    else:
        print("[red]Tendência: BAIXA 📉[/red]")

    relatorio = pd.DataFrame({
        "Preço": [preco],
        "MM20": [mm20],
        "MM50": [mm50],
        "RSI": [rsi]
    })

    relatorio.to_csv(
        f"relatorios/{ticker}.csv",
        index=False
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        dados.index,
        dados["Close"],
        label="Preço"
    )

    plt.plot(
        dados.index,
        dados["MM20"],
        label="MM20"
    )

    plt.plot(
        dados.index,
        dados["MM50"],
        label="MM50"
    )

    plt.title(ticker)

    plt.legend()

    plt.grid()

    plt.savefig(
        f"graficos/{ticker}.png"
    )

    plt.show()

    print(
        f"\n[green]Relatório salvo em relatorios/{ticker}.csv[/green]"
    )

    print(
        f"[green]Gráfico salvo em graficos/{ticker}.png[/green]"
    )