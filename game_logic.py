import random

def calcular_aposta_bot(bot_atual, mesa_jogadores):
    """
    Calcula dinamicamente o valor da aposta de um bot com base no cenário atual da mesa.
    Agora, o bot também considera se o seu saldo é confortável em relação aos outros.
    """
    # Filtra e extrai apenas o saldo dos oponentes na mesa
    saldos_adversarios = [j["saldo"] for j in mesa_jogadores if j["nome"] != bot_atual["nome"]]
    maior_saldo_mesa = max(saldos_adversarios) if saldos_adversarios else 0
    
    # Bloco de decisão estratégica do bot baseado no seu patrimônio na mesa
    if bot_atual["saldo"] > maior_saldo_mesa:
        # Perfil Agressivo: Se tem mais fichas que todos, arrisca uma fatia maior (até 50% do saldo)
        limite_superior = max(2.0, bot_atual["saldo"] * 0.5)
        aposta = round(random.uniform(1.0, limite_superior), 2)
        print(f"[Bot] {bot_atual['nome']}: 'Estou na vantagem, vou pressionar a mesa.'")
    else:
        # Perfil Defensivo: Se está atrás, joga seguro limitando-se a 10% das suas fichas
        limite_seguro = bot_atual["saldo"] * 0.1
        aposta = round(random.uniform(1.0, max(1.0, limite_seguro)), 2)
        print(f"[Bot] {bot_atual['nome']}: 'Eles têm mais dinheiro, vou jogar na defensiva.'")
        
    return aposta