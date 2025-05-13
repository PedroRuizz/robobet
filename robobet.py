import random
import matplotlib.pyplot as plt
import csv

# Função para gerar jogos aleatórios
def gerar_jogos(qtd):
    times = ["Time A", "Time B", "Time C", "Time D", "Time E", "Time F", "Time G", "Time H", "Time I", "Time J"]
    jogos = []
    for _ in range(qtd):
        casa = random.choice(times)
        fora = random.choice([t for t in times if t != casa])
        odd = round(random.uniform(1.5, 3.0), 2)
        prob = round(random.uniform(0.4, 0.65), 2)
        jogos.append({"casa": casa, "fora": fora, "odd": odd, "prob": prob})
    return jogos

# Parâmetros
jogos = gerar_jogos(100)
banca = 100
valor_aposta = 10
lucro_total = 0
evolucao_banca = [banca]
historico = []

# Simulação
for i, jogo in enumerate(jogos, start=1):
    odd = jogo["odd"]
    prob = jogo["prob"]
    esperado = prob * odd
    aposta_feita = False
    lucro_aposta = 0
    resultado = "Não apostou"

    if esperado > 1:
        aposta_feita = True
        banca -= valor_aposta
        vitoria = random.random() < prob

        if vitoria:
            ganho = valor_aposta * (odd - 1)
            lucro_total += ganho
            banca += valor_aposta + ganho
            lucro_aposta = ganho
            resultado = "Vitória"
        else:
            lucro_total -= valor_aposta
            lucro_aposta = -valor_aposta
            resultado = "Derrota"

    evolucao_banca.append(banca)

    historico.append({
        "Aposta": i,
        "Jogo": f"{jogo['casa']} x {jogo['fora']}",
        "Odd": odd,
        "Probabilidade": prob,
        "Esperado": round(esperado, 2),
        "Resultado": resultado,
        "Lucro/Prejuízo": round(lucro_aposta, 2),
        "Banca": round(banca, 2)
    })

# Salva histórico em CSV
with open("historico_apostas.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=historico[0].keys())
    writer.writeheader()
    writer.writerows(historico)

print(f"\nSimulação finalizada. Lucro total: R${lucro_total:.2f} | Banca final: R${banca:.2f}")
print("Arquivo 'historico_apostas.csv' salvo com os resultados.")

# Gráfico
plt.figure(figsize=(10, 5))
plt.plot(evolucao_banca, marker='o', linestyle='-', color='green')
plt.title("Evolução da Banca (100 apostas)")
plt.xlabel("Número de Apostas")
plt.ylabel("Valor da Banca (R$)")
plt.grid(True)
plt.show()
