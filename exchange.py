import random

# Dados do investidor
NOME = "Investidor"
CPF = "12345678900"
SENHA = "123456"

# Cotações iniciais (valores de exemplo em reais)
cotacoes = {
    "bitcoin": 350000.00,
    "ethereum": 13000.00,
    "ripple": 3.00
}

taxa_compra = {
    "bitcoin": 0.02,
    "ethereum": 0.01,
    "ripple": 0.01
}

taxa_venda = {
    "bitcoin": 0.03,
    "ethereum": 0.02,
    "ripple": 0.01
}

# Carrega os saldos salvos ou cria saldos zerados
try:
    arquivo = open("saldo.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    reais = float(linhas[0])
    bitcoin = float(linhas[1])
    ethereum = float(linhas[2])
    ripple = float(linhas[3])
except:
    reais = 0.0
    bitcoin = 0.0
    ethereum = 0.0
    ripple = 0.0

# Carrega as cotações salvas
try:
    arquivo = open("cotacoes.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    cotacoes["bitcoin"] = float(linhas[0])
    cotacoes["ethereum"] = float(linhas[1])
    cotacoes["ripple"] = float(linhas[2])
except:
    pass


def salvar_saldo():
    arquivo = open("saldo.txt", "w")
    arquivo.write(str(reais) + "\n")
    arquivo.write(str(bitcoin) + "\n")
    arquivo.write(str(ethereum) + "\n")
    arquivo.write(str(ripple) + "\n")
    arquivo.close()


def salvar_cotacoes():
    arquivo = open("cotacoes.txt", "w")
    arquivo.write(str(cotacoes["bitcoin"]) + "\n")
    arquivo.write(str(cotacoes["ethereum"]) + "\n")
    arquivo.write(str(cotacoes["ripple"]) + "\n")
    arquivo.close()


def registrar_extrato(mensagem):
    arquivo = open("extrato.txt", "a")
    arquivo.write(mensagem + "\n")
    arquivo.close()


def consultar_saldo():
    global reais, bitcoin, ethereum, ripple

    senha = input("Digite sua senha: ")
    if senha == SENHA:
        print("\n--- SALDO DA CARTEIRA ---")
        print("Nome:", NOME)
        print("CPF:", CPF)
        print("Reais: R$", round(reais, 2))
        print("Bitcoin:", round(bitcoin, 8))
        print("Ethereum:", round(ethereum, 8))
        print("Ripple:", round(ripple, 8))
    else:
        print("Senha incorreta.")


def consultar_extrato():
    senha = input("Digite sua senha: ")
    if senha == SENHA:
        print("\n--- EXTRATO ---")
        try:
            arquivo = open("extrato.txt", "r")
            conteudo = arquivo.read()
            arquivo.close()
            if conteudo == "":
                print("Nenhuma operação realizada.")
            else:
                print(conteudo)
        except:
            print("Nenhuma operação realizada.")
    else:
        print("Senha incorreta.")


def depositar():
    global reais
    try:
        valor = float(input("Valor do depósito: R$ "))
        if valor > 0:
            reais = reais + valor
            salvar_saldo()
            registrar_extrato("Depósito: R$ " + str(round(valor, 2)))
            print("Depósito realizado!")
            print("Saldo em reais: R$", round(reais, 2))
        else:
            print("Digite um valor maior que zero.")
    except:
        print("Valor inválido.")


def sacar():
    global reais
    try:
        valor = float(input("Valor do saque: R$ "))
        if valor <= 0:
            print("Digite um valor maior que zero.")
        elif valor > reais:
            print("Saldo insuficiente.")
        else:
            reais = reais - valor
            salvar_saldo()
            registrar_extrato("Saque: R$ " + str(round(valor, 2)))
            print("Saque realizado!")
            print("Saldo em reais: R$", round(reais, 2))
    except:
        print("Valor inválido.")


def mostrar_cotacoes():
    print("\n--- COTAÇÕES ---")
    print("Bitcoin: R$", round(cotacoes["bitcoin"], 2))
    print("Ethereum: R$", round(cotacoes["ethereum"], 2))
    print("Ripple: R$", round(cotacoes["ripple"], 2))


def comprar():
    global reais, bitcoin, ethereum, ripple

    senha = input("Digite sua senha: ")
    if senha != SENHA:
        print("Senha incorreta.")
        return

    mostrar_cotacoes()
    moeda = input("Qual moeda deseja comprar (bitcoin, ethereum ou ripple)? ").lower()

    if moeda not in cotacoes:
        print("Moeda inválida.")
        return

    try:
        valor = float(input("Quanto deseja gastar em reais? R$ "))
        taxa = taxa_compra[moeda]
        total = valor * (1 + taxa)

        if valor <= 0:
            print("Digite um valor maior que zero.")
        elif total > reais:
            print("Saldo em reais insuficiente, incluindo a taxa.")
        else:
            quantidade = valor / cotacoes[moeda]

            reais = reais - total

            if moeda == "bitcoin":
                bitcoin = bitcoin + quantidade
            elif moeda == "ethereum":
                ethereum = ethereum + quantidade
            else:
                ripple = ripple + quantidade

            salvar_saldo()
            registrar_extrato(
                "Compra de " + moeda + ": " + str(quantidade)
                + " | Valor: R$ " + str(round(valor, 2))
                + " | Taxa: R$ " + str(round(valor * taxa, 2))
            )
            print("Compra realizada!")
            print("Quantidade comprada:", round(quantidade, 8))
            print("Total descontado: R$", round(total, 2))
    except:
        print("Valor inválido.")


def vender():
    global reais, bitcoin, ethereum, ripple

    senha = input("Digite sua senha: ")
    if senha != SENHA:
        print("Senha incorreta.")
        return

    mostrar_cotacoes()
    moeda = input("Qual moeda deseja vender (bitcoin, ethereum ou ripple)? ").lower()

    if moeda not in cotacoes:
        print("Moeda inválida.")
        return

    try:
        quantidade = float(input("Qual quantidade deseja vender? "))
        if moeda == "bitcoin":
            saldo_moeda = bitcoin
        elif moeda == "ethereum":
            saldo_moeda = ethereum
        else:
            saldo_moeda = ripple

        if quantidade <= 0:
            print("Digite uma quantidade maior que zero.")
        elif quantidade > saldo_moeda:
            print("Você não possui essa quantidade.")
        else:
            valor = quantidade * cotacoes[moeda]
            taxa = valor * taxa_venda[moeda]
            valor_recebido = valor - taxa

            if moeda == "bitcoin":
                bitcoin = bitcoin - quantidade
            elif moeda == "ethereum":
                ethereum = ethereum - quantidade
            else:
                ripple = ripple - quantidade

            reais = reais + valor_recebido
            salvar_saldo()
            registrar_extrato(
                "Venda de " + moeda + ": " + str(quantidade)
                + " | Valor: R$ " + str(round(valor, 2))
                + " | Taxa: R$ " + str(round(taxa, 2))
                + " | Recebido: R$ " + str(round(valor_recebido, 2))
            )
            print("Venda realizada!")
            print("Valor recebido: R$", round(valor_recebido, 2))
    except:
        print("Valor inválido.")


def atualizar_cotacoes():
    for moeda in cotacoes:
        variacao = random.uniform(-0.05, 0.05)
        cotacoes[moeda] = cotacoes[moeda] * (1 + variacao)

    salvar_cotacoes()
    print("Cotações atualizadas!")
    mostrar_cotacoes()


# LOGIN
print("=== EXCHANGE DE CRIPTOMOEDAS ===")
cpf_digitado = input("Digite seu CPF (somente números): ")
senha_digitada = input("Digite sua senha de 6 dígitos: ")

if cpf_digitado == CPF and senha_digitada == SENHA:
    print("\nLogin realizado com sucesso!")

    opcao = 0
    while opcao != 8:
        print("\n===== MENU =====")
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar reais")
        print("4 - Sacar reais")
        print("5 - Comprar criptomoedas")
        print("6 - Vender criptomoedas")
        print("7 - Atualizar cotações")
        print("8 - Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
        except:
            opcao = 0

        if opcao == 1:
            consultar_saldo()
        elif opcao == 2:
            consultar_extrato()
        elif opcao == 3:
            depositar()
        elif opcao == 4:
            sacar()
        elif opcao == 5:
            comprar()
        elif opcao == 6:
            vender()
        elif opcao == 7:
            atualizar_cotacoes()
        elif opcao == 8:
            print("Programa encerrado.")
        else:
            print("Opção inválida.")
else:
    print("CPF ou senha incorretos.")
