from time import sleep
import random

# =====================================================================
# 1. ÁREA DE FUNÇÕES (As ferramentas organizadas e seguras)
# =====================================================================

def exibir_boas_vindas():
    """Mostra a tela inicial do Cassino."""
    print('*' * 30)
    print('Seja Bem Vindo ao Cassino\nDivirta-se !')
    print('*' * 30)


def exibir_regras():
    """Explica as regras de aposta do jogo."""
    print('\nRegras de aposta :')
    print('1 - Não pode apostar um valor menor ou igual a Zero')
    print('2 - Não pode apostar um valor maior que o Deposito feito')
    print('Bom Jogo !')


def fazer_deposito():
    """Pede o depósito inicial garantindo que seja um número válido maior que zero."""
    while True:
        try:
            valor = float(input('Digite o Valor do seu deposito: R$ '))
            if valor > 0:
                return valor
            else:
                print('O valor do depósito deve ser maior que zero.')
        except ValueError:
            print('Entrada inválida! Por favor, digite apenas números.')


def jogar_rodada(aposta):
    """Roda a lógica do sorteio e do palpite. Devolve 'ganhou' ou 'perdeu'."""
    print('\nBem vindo ao jogo de advinhação !')
    print('Eu vou escolher um numero de 1 a 5, se você acertar, dobra seu saldo.')
    print('Vou escolher um número...')
    
    pc = random.randint(1, 5)
    sleep(2)
    print('Pronto, qual número pensei ?')
    
    while True:
        try:
            player = int(input('Digite o número que ele pensou: '))
            if 1 <= player <= 5:
                break
            print('Por favor, escolha um número entre 1 e 5.')
        except ValueError:
            print('Entrada inválida! Digite um número inteiro de 1 a 5.')

    if player == pc:
        print(f'Parabéns, eu também pensei em {pc}, você ganhou !')
        return "ganhou"
    else:
        print(f'Eu pensei no numero {pc}, você perdeu')
        return "perdeu"


# =====================================================================
# 2. PROGRAMA PRINCIPAL (Onde o jogo realmente roda)
# =====================================================================

exibir_boas_vindas()
exibir_regras()

# Guardamos o valor validado na nossa variável principal de saldo
deposito = fazer_deposito()

print('Processando Deposito...')
sleep(2)
print('Deposito Concluido')
print(f'Seu saldo atual é de R$ {deposito:.2f}\n')

# Loop principal das rodadas
while True:
    try:
        aposta = float(input('Deseja apostar quanto ? '))
    except ValueError:
        print('Por favor, digite um valor numérico para a aposta.')
        continue

    # Validação da aposta usando o saldo atual (deposito)
    if aposta <= 0 or aposta > deposito:
        print('Aposta invalida, faça uma aposta dentro do valor depositado')
        continue

    print('Aposta Aceita !\nVamos Começar ')

    # Executa a rodada e captura o resultado ("ganhou" ou "perdeu")
    resultado = jogar_rodada(aposta)

    # Atualiza a carteira do jogador com base no resultado da função
    if resultado == "ganhou":
        deposito += aposta
    else:
        deposito -= aposta

    print(f'Seu novo saldo é de R$ {deposito:.2f}')

    # Verificando se o saldo acabou
    if deposito <= 0:
        print('Seu saldo chegou a zero, não foi dessa vez. Obrigado por Jogar !')
        break

    # Finalizar ou continuar o jogo
    print('-' * 40)
    resposta = input('Deseja continuar jogando? [S/N]: ').upper().strip()
    
    if resposta in ['N', 'NÃO', 'NAO']:
        print(f'\nMuito Obrigado por jogar com a gente. Você está saindo com R$ {deposito:.2f}, esperamos você em breve!')
        break
