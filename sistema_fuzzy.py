import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Definindo as variáveis fuzzy
qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

# Funções de pertinência
qualidade['ruim'] = fuzz.trimf(qualidade.universe, [0, 0, 5])
qualidade['regular'] = fuzz.trimf(qualidade.universe, [0, 5, 10])
qualidade['bom'] = fuzz.trimf(qualidade.universe, [5, 10, 10])

servico['ruim'] = fuzz.trimf(servico.universe, [0, 0, 5])
servico['regular'] = fuzz.trimf(servico.universe, [0, 5, 10])
servico['bom'] = fuzz.trimf(servico.universe, [5, 10, 10])

gorjeta['baixa'] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta['alta'] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

# Regras fuzzy
regra1 = ctrl.Rule(qualidade['ruim'] | servico['ruim'], gorjeta['baixa'])
regra2 = ctrl.Rule(qualidade['regular'] | servico['regular'], gorjeta['media'])
regra3 = ctrl.Rule(qualidade['bom'] | servico['bom'], gorjeta['alta'])

# Sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema_simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Menu principal
print("=-" * 20)
print("\t\tCalculadora de Gorjeta")
print("-=" * 20)

while True:
    try:
        # Entrada do usuário
        qualidade_input = int(input("Digite a avaliação da qualidade (entre 0 e 10): "))
        servico_input = int(input("Digite a avaliação do serviço (entre 0 e 10): "))
        
        if not (0 <= qualidade_input <= 10 and 0 <= servico_input <= 10):
            raise ValueError("Os valores devem estar entre 0 e 10.")

        # Configurando entradas no sistema fuzzy
        sistema_simulacao.input['qualidade'] = qualidade_input
        sistema_simulacao.input['servico'] = servico_input
        sistema_simulacao.compute()

        # Calculando a gorjeta
        valor_gorjeta = round(sistema_simulacao.output['gorjeta'], 2)
        gorjeta_formatada = locale.currency(valor_gorjeta, grouping=True)

        # Classificando atendimento
        if qualidade_input <= 5 and servico_input <= 5:
            atendimento = "Ruim"
        elif 5 < qualidade_input < 10 or 5 < servico_input < 10:
            atendimento = "Regular"
        else:
            atendimento = "Ótimo"

        # Exibindo resultado
        print(f"\nAtendimento: {atendimento}")
        print(f"Gorjeta sugerida: {gorjeta_formatada}")

        # Continuar ou sair
        continuar = input("\nDeseja calcular outra gorjeta? (S/N): ").strip().lower()
        if continuar != 's':
            break

    except ValueError as e:
        print(f"Erro: {e}. Tente novamente.")

# Mensagem final
print("\nObrigado por usar a Calculadora de Gorjetas!")
