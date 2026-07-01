import random
from time import sleep
from game_logic import calcular_aposta_bot
from auth import sistema_login, carregar_banco_dados, salvar_banco_dados

print('=' * 40)
print('          CASSINO PYTHON V2          ')
print('=' * 40)

# Inicialização e autenticação do jogador ativo
nome_usuario, saldo_usuario = sistema_login()
sleep(1)

# Lista de dicionários que representa as entidades da mesa corrente
mesa_jogadores = [
    {"nome": nome_usuario, "saldo": saldo_usuario, "eh_bot": False},
    {"nome": "Bot_Cabuloso", "saldo": 80.0, "eh_bot": True},
    {"nome": "Bot_Prudente", "saldo": 120.0, "eh_bot": True},
    {"nome": "Bot_Zangado", "saldo": 50.0, "eh_bot": True}
]

# Loop central que mantém o fluxo do torneio ativo
while len(mesa_jogadores) > 0:
    print(f"\nNova rodada iniciada. Jogadores na mesa: {len(mesa_jogadores)}")
    
    # Definição do Alvo/Gabarito da rodada corrente
    numero_secreto = random.randint(1, 10)
    
    # Dicionários temporários para armazenar as jogadas da rodada atual
    palpites_rodada = {}
    apostas_rodada = {}
    
    # Fase de coleta de dados de todos os participantes
    for jogador in mesa_jogadores:
        nome = jogador["nome"]
        
        if jogador["eh_bot"]:
            # Processamento automatizado para inteligência artificial do bot
            valor_aposta = calcular_aposta_bot(jogador, mesa_jogadores)
            palpite = random.randint(1, 10)
            
            apostas_rodada[nome] = valor_aposta
            palpites_rodada[nome] = palpite
            print(f"[Bot] {nome} apostou R$ {valor_aposta:.2f} no número {palpite}.")
            sleep(0.5)
        else:
            # Entrada controlada de dados para o jogador humano
            while True:
                print(f"\nSua vez, {nome}. Saldo atual: R$ {jogador['saldo']:.2f}")
                try:
                    valor_aposta = float(input('Deseja apostar quanto? R$ '))
                    # Validação de regras básicas de aposta e margem de saldo
                    if valor_aposta <= 0 or valor_aposta > jogador["saldo"]:
                        print('Aposta inválida. Verifique seu saldo disponível.')
                        continue
                    
                    palpite = int(input('Escolha seu palpite (1 a 10): '))
                    if palpite < 1 or palpite > 10:
                        print('Escolha um número válido entre 1 e 10.')
                        continue
                        
                    apostas_rodada[nome] = valor_aposta
                    palpites_rodada[nome] = palpite
                    break
                except ValueError:
                    print('Erro: Por favor, digite apenas números válidos.')

    print('\nO computador está sorteando o número...')
    sleep(1.5)
    print(f"O número secreto era: {numero_secreto}\n")
    print('--- RESULTADOS DA RODADA ---')
    
    # ─── LÓGICA DE JOGO DE MESA COM POTE ───
    pote_total = 0.0
    vencedores = []
    
    # Primeiro recolhe as apostas e define quem acertou
    for jogador in mesa_jogadores:
        nome = jogador["nome"]
        aposta = apostas_rodada[nome]
        palpite = templates = palpites_rodada[nome]
        
        jogador["saldo"] -= aposta
        pote_total += aposta
        
        if palpite == numero_secreto:
            vencedores.append(jogador)
            
    # Distribuição do prêmio do Pote
    if len(vencedores) > 0:
        premio_por_vencedor = pote_total / len(vencedores)
        
        # Mostra quem errou primeiro
        for jogador in mesa_jogadores:
            if jogador not in vencedores:
                print(f"[ERRO] {jogador['nome']} errou. Perdeu R$ {apostas_rodada[jogador['nome']]:.2f}. Saldo: R$ {jogador['saldo']:.2f}")
                
        # Distribui o prêmio para os vencedores
        for ganhador in vencedores:
            ganhador["saldo"] += premio_por_vencedor
            print(f"[ACERTO] {ganhador['nome']} ACERTOU! Levou R$ {premio_por_vencedor:.2f} do pote. Novo Saldo: R$ {ganhador['saldo']:.2f}")
    else:
        print(f"Nenhum jogador acertou o número. O pote de R$ {pote_total:.2f} acumulou para a banca.")
        for jogador in mesa_jogadores:
            print(f"[ERRO] {jogador['nome']} errou. Perdeu R$ {apostas_rodada[jogador['nome']]:.2f}. Saldo: R$ {jogador['saldo']:.2f}")

    # Captura o saldo do humano antes de qualquer remoção ou desistência para evitar erros de persistência
    saldo_humano_atual = 0.0
    humano_esta_vivo = False
    for jogador in mesa_jogadores:
        if not jogador["eh_bot"]:
            saldo_humano_atual = jogador["saldo"]
            if saldo_humano_atual > 0:
                humano_esta_vivo = True

    # Limpeza da mesa: Remove quem faliu (saldo zerado)
    mesa_jogadores = [j for j in mesa_jogadores if j["saldo"] > 0]
    
    jogadores_ativos = []
    humano_quer_continuar = False
    
    # Processamento de permanência na mesa
    for jogador in mesa_jogadores:
        if jogador["eh_bot"]:
            jogadores_ativos.append(jogador)
        else:
            resposta = input(f"\n{jogador['nome']}, deseja continuar jogando? (s/n): ").lower()
            if resposta == 's':
                jogadores_ativos.append(jogador)
                humano_quer_continuar = True
            else:
                print(f"Você escolheu sair da mesa com R$ {jogador['saldo']:.2f}.")
                # Salva o saldo imediatamente se ele decidiu sair por vontade própria
                banco = carregar_banco_dados()
                banco[nome_usuario]["saldo"] = jogador["saldo"]
                salvar_banco_dados(banco)

    mesa_jogadores = jogadores_ativos

    # Se o humano saiu voluntariamente ou faliu (não sobrou humano ativo querendo jogar)
    if not humano_quer_continuar:
        # Se ele não quer continuar mas ainda tinha saldo (saiu voluntariamente), o saldo já foi salvo acima.
        # Mas se ele foi eliminado por falta de saldo, salvamos o zero definitivo aqui.
        if not humano_esta_vivo:
            banco = carregar_banco_dados()
            banco[nome_usuario]["saldo"] = 0.0
            salvar_banco_dados(banco)
            print("\nO torneio acabou para você. Seu saldo zerou.")
        break

print('\nFim do jogo. Obrigado por jogar.')