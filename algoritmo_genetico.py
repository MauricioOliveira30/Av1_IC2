import random
import requests

# Dados iniciais
criptomoedas = []
TAM = int(input("Digite quantas criptomoedas quer avaliar:"))
i = 1
while i <= TAM:
    i += 1
    cripto = input("Digite as criptos que deseja avaliar ou digite sair (para sair): ")

    historico_retornos = [
        [1.31, 0.11, 0.02, 0.01, 0.04],  # Retornos históricos para o período 1
        [0.66, 0.05, 0.05, 0.03, 0.02],  # Retornos históricos para o período 2
        [0.73, 0.03, 0.04, 0.02, 0.05]  # Retornos históricos para o período 3
    ]
    if cripto == "sair":
        break
    criptomoedas.append(cripto)


# Parâmetros do algoritmo genético
TAM_POPULAÇÃO = 100
NUM_GERAÇÃO = 50
TAXA_MUTAÇÃO = 0.01


# Função para obter a cotação de uma criptomoeda
def get_cotacao(criptomoedas):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={criptomoedas}&vs_currencies=BRL"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if criptomoedas in data:
            return data[criptomoedas]["BRL"]
    return None


# Função de avaliação (fitness)
def evolução(indivíduo):
    retorno_total = 0
    for periodo in historico_retornos:
        retorno_periodo = sum([retorno * peso for retorno, peso in zip(periodo, indivíduo)])
        retorno_total += retorno_periodo
    return retorno_total


# Inicialização da população
def criador_indivíduo():
    return [random.uniform(0, 1) for _ in range(len(criptomoedas))]


população = []

# Criação da população inicial
for _ in range(TAM_POPULAÇÃO):
    indivíduo = criador_indivíduo()
    população.append(indivíduo)

# Loop principal do algoritmo genético
for generation in range(NUM_GERAÇÃO):
    # Avaliação da aptidão (fitness)
    aptidão = [evolução(indivíduo) for indivíduo in população]
# Seleção dos indivíduos para reprodução
selecionados_pais = random.choices(população, weights=aptidão, k=TAM_POPULAÇÃO)

# Reprodução (cruzamento e mutação)
offspring = []
for i in range(0, TAM_POPULAÇÃO, 2):
    pai1 = selecionados_pais[i]
    pai2 = selecionados_pais[i + 1]
    filho1 = pai1[:]
    filho2 = pai2[:]

    # Cruzamento (recombinação)
    ponto_crossover = random.randint(1, len(criptomoedas) - 1)
    filho1[ponto_crossover:] = pai2[ponto_crossover:]
    filho2[ponto_crossover:] = pai1[ponto_crossover:]

    # Mutação
    for j in range(len(criptomoedas)):
        if random.random() < TAXA_MUTAÇÃO:
            filho1[j] = random.uniform(0, 1)
            filho2[j] = random.uniform(0, 1)

    offspring.append(filho1)
    offspring.append(filho2)
# Substituição da população antiga pela nova
população = offspring
# Encontrar o indivíduo mais apto na população final
melhor_indivíduo = max(população, key=evolução)

# Exibir o resultado
print("Alocação ótima de investimentos em criptomoedas:")
for i in range(len(criptomoedas)):
    print(f"{criptomoedas[i]}: {melhor_indivíduo[i] * 100:.2f}%")
