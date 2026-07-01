import json
import os

# Constante global que define o arquivo de persistência de dados
ARQUIVO_BANCO = "usuarios.json"

def carregar_banco_dados():
    """
    Verifica a existência do arquivo JSON. Cria um banco de dados
    vazio caso não exista e trata exceções de formatação de texto.
    """
    if not os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        return {}
    
    try:
        with open(ARQUIVO_BANCO, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Retorna dicionário vazio caso o arquivo esteja corrompido ou mal formatado
        return {}

def salvar_banco_dados(dados):
    """Grava o estado atualizado do dicionário de usuários no arquivo físico JSON."""
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def sistema_login():
    """
    Gerencia a autenticação do usuário, permitindo a persistence do saldo anterior
    ou forçando um novo aporte financeiro caso o usuário seja novo ou esteja falido.
    """
    banco = carregar_banco_dados()
    
    print("\n--- SISTEMA DE LOGIN ---")
    usuario = input("Digite seu nome de usuário: ").strip()
    
    # Fluxo para usuário existente no sistema
    if usuario in banco:
        print(f"Bem-vindo de volta, {usuario}.")
        print(f"Seu saldo recuperado é de: R$ {banco[usuario]['saldo']:.2f}")
        
        # Validação de restrição para contas com saldo zerado
        if banco[usuario]['saldo'] <= 0:
            print("Aviso: Seu saldo está zerado. Faça um novo depósito para entrar na mesa.")
            while True:
                try:
                    novo_deposito = float(input("Digite o valor do depósito: R$ "))
                    if novo_deposito > 0:
                        banco[usuario]['saldo'] = novo_deposito
                        salvar_banco_dados(banco)
                        break
                    print("Erro: O depósito precisa ser maior que zero.")
                except ValueError:
                    print("Erro: Digite um número válido.")
                    
    # Fluxo para cadastro de novo usuário
    else:
        print(f"Usuário '{usuario}' não encontrado. Criando nova conta...")
        while True:
            try:
                deposito_inicial = float(input("Digite o valor do seu depósito inicial: R$ "))
                if deposito_inicial > 0:
                    break
                print("Erro: O depósito inicial precisa ser maior que zero.")
            except ValueError:
                print("Erro: Digite um número válido.")
        
        # Inicializa a estrutura do usuário dentro do dicionário global do banco
        banco[usuario] = {"saldo": deposito_inicial}
        salvar_banco_dados(banco)
        print(f"Conta criada com sucesso para {usuario}.")

    return usuario, banco[usuario]['saldo']