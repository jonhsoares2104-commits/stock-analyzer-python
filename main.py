from analisador import analisar_acao


while True:

    print("\n=== STOCK ANALYZER ===")

    print("1 - Analisar")
    print("2 - Sair")

    opcao = input("\nEscolha: ")

    if opcao == "1":

        ticker = input(
            "Ticker (PETR4.SA): "
        ).upper()

        analisar_acao(ticker)

    elif opcao == "2":

        break