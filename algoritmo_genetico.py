import random
from deap import algorithms, base, creator, tools
import matplotlib.pyplot as plt

# Definindo a função de fitness
def evaluate_portfolio(individual):
    cryptocurrencies = ['BTC', 'ETH', 'XRP', 'LTC', 'ADA']

    # Dados históricos de preços das criptomoedas (exemplo fictício)
    price_data = {
        'BTC': [10000, 11000, 12000, 13000, 14000],
        'ETH': [200, 220, 240, 260, 280],
        'XRP': [0.3, 0.32, 0.35, 0.38, 0.4],
        'LTC': [50, 55, 60, 65, 70],
        'ADA': [0.1, 0.11, 0.12, 0.13, 0.14]
    }

    # Calculando o valor total da carteira inicialmente como zero
    portfolio_value = 0

    # Calculando o valor total da carteira
    for crypto, weight in zip(cryptocurrencies, individual):
        price_history = price_data[crypto]
        price = price_history[-1]  # Usando o último preço disponível como referência
        portfolio_value += weight * price

    # Calculando o lucro como a diferença entre o valor atual da carteira e um valor de referência (exemplo fictício)
    reference_value = 10000  # Valor inicial da carteira
    profit = portfolio_value - reference_value

    return profit,
    return fitness_value,


# Definindo o tamanho da população e o número de gerações
POPULATION_SIZE = 100
NUM_GENERATIONS = 50

# Definindo o número de criptomoedas na carteira
NUM_CRYPTOCURRENCIES = 5

# Definindo os limites superiores e inferiores para os pesos das criptomoedas
LOWER_BOUND = 0.0
UPPER_BOUND = 1.0

# Criando os tipos de fitness e indivíduo utilizando a biblioteca DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Criando a caixa de ferramentas (toolbox) com as funções de inicialização, mutação, cruzamento e avaliação
toolbox = base.Toolbox()
toolbox.register("attribute", random.uniform, LOWER_BOUND, UPPER_BOUND)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=NUM_CRYPTOCURRENCIES)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_portfolio)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    # Inicializando a população
    population = toolbox.population(n=POPULATION_SIZE)

    # Avaliando todos os indivíduos na população
    fitness_values = map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitness_values):
        ind.fitness.values = fit

    # Definindo a taxa de cruzamento, mutação e o número de indivíduos a serem selecionados para a próxima geração
    CXPB, MUTPB, N_SELECTED = 0.5, 0.2, 10

    # Rodando o algoritmo genético
    for generation in range(NUM_GENERATIONS):
        print("Generation", generation)

        # Selecionando os indivíduos para a próxima geração
        offspring = toolbox.select(population, N_SELECTED)

        # Realizando o cruzamento e a mutação
        offspring = algorithms.varAnd(offspring, toolbox, cxpb=CXPB, mutpb=MUTPB)

        # Avaliando os novos indivíduos
        fitness_values = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitness_values):
            ind.fitness.values = fit

        # Substituindo a população atual pelos novos indivíduos
        population[:] = offspring

        # Extraindo os valores de fitness da população atual
        fitnesses = [ind.fitness.values[0] for ind in population]

        # Imprimindo a melhor solução encontrada na geração atual
        best_index = fitnesses.index(max(fitnesses))
        print("Best portfolio:", population[best_index])
        print("Best fitness:", max(fitnesses))
        print("--------------------------")
plt.plot(range(NUM_GENERATIONS) )
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Evolution of Best Fitness")
plt.show()

if __name__ == "__main__":
    main()
