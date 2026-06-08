from time import sleep
import random

#Tela de Boas Vindas

print ('*' * 30)
print ('Seja Bem Vindo ao Cassino\nDivirta-se !')
print ('*' * 30)

print ('Regras de aposta :\n1 - Não pode apostar um valor menor ou igual a Zero' \
'\n2 - Não pode apostar um valor maior que o Deposito feito\nBom Jogo !')

#Pedir para um usuario depositar um valor 

saldo = float (input ('Digite o Valor do seu deposito: '))
deposito = saldo
print ('Processando Deposito...')
sleep (2)
print ('Deposito Concluido')

print (f'Seu saldo atual é de R$ {deposito}\n')


#Adicionar os Loops 

while True:
    aposta = float (input('Deseja apostar quanto ? '))

    if aposta <= 0 or aposta > deposito:
        print ('Aposta invalida, faça uma aposta dentro do valor depositado')
        continue

    else: 
        print ('Aposta Aceita !\nVamos Começar ')

#Iniciando o Jogo 

    print ('\nBem vindo ao jogo de advinhação !\n' \
    'Eu vou escolher um numero de 1 a 5, se você acertar, dobra seu saldo, se errar, tente de novo\n' \
    'Vamos começar ?\n')

    print ('Vou escolher um número...')
    pc = random. randint (1,5)
    sleep (2)
    print ('Pronto, qual número pensei ?')

#Player Jogando

    player = int (input ('Digite o número que ele pensou :\n'))
    if ( player == pc):
        print (f'Parabéns, eu também pensei em {pc}, você ganhou !')
        deposito += aposta
        print (f'Seu novo saldo é de: R${deposito}')

    else:
        print (f'Eu pensei no numero {pc}, você perdeu')
        deposito -= aposta
        print (f'Seu novo saldo é de R$ {deposito}')

#Verificando saldo

    if deposito <= 0:
        print ('Seu saldo chegou a zero, não foi dessa vez. Obrigado por Jogar !')
        break

#finalizar ou continuar game

    print('-' * 40)
    resposta = input('Deseja continuar jogando? [S/N]: ').upper().strip()
    
# Se ele digitar N ou Não, o jogo para
    if resposta == 'N' or resposta == 'NÃO':
        print(f'\nMuito Obrigado por jogar com a gente. Você está saindo com R$ {deposito:.2f}, esperamos você em breve!')
        break
