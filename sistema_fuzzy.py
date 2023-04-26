# Bibliotecas
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Lógica Fuzzy
qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade')

serviço = ctrl.Antecedent(np.arange(0, 11, 1), 'serviço')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')
qualidade['ruim'] = fuzz.trimf(qualidade.universe, [0, 0, 5])
qualidade['regular'] = fuzz.trimf(qualidade.universe, [0, 5, 10])
qualidade['bom'] = fuzz.trimf(qualidade.universe, [5, 10, 10])

serviço['ruim'] = fuzz.trimf(serviço.universe, [0, 0, 5])
serviço['regular'] = fuzz.trimf(serviço.universe, [0, 5, 10])
serviço['bom'] = fuzz.trimf(serviço.universe, [5, 10, 10])

gorjeta['baixa'] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta['alta'] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

# Regras de negócio
regra1 = ctrl.Rule(qualidade['ruim'] | serviço['ruim'], gorjeta['baixa'])
regra2 = ctrl.Rule(qualidade['regular'] | serviço['regular'], gorjeta['media'])
regra3 = ctrl.Rule(qualidade['bom'] | serviço['bom'], gorjeta['alta'])
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema_gorjeta = ctrl.ControlSystemSimulation(sistema_controle)

# Menu
print("=-" * 20)
print("\t\t\tCalculadora de Gorjeta\t\t\t")
print("-=" * 20)

while True:
    atendimento = ""
    while True:
        qualidade = input("Digite a avaliação da qualidade (entre 0 e 10): ")
        serviço = input("Digite a avaliação do serviço (entre 0 e 10): ")
        if not qualidade.isnumeric() and not serviço.isnumeric():
            print("Por favor, digite um valor numérico.")
        else:
            qualidade = float(qualidade)
            serviço = float(serviço)
    

        if  (0 > qualidade or qualidade> 10 and  0 > serviço or serviço> 10):
         print("Digite um valor entre 0 e 10:")

        else:
            break

    sistema_gorjeta.input['qualidade'] = qualidade
    sistema_gorjeta.input['serviço'] = serviço
    sistema_gorjeta.compute()
    valor_gorjeta = locale.currency(
        float(str(sistema_gorjeta.output['gorjeta'])))

    # Atendimento
    if 0 <= qualidade <= 5 and 0 <= serviço <= 5:
        valor_gorjeta = locale.currency(
            float(str(sistema_gorjeta.output['gorjeta']).replace('R$', '').replace(',', '.')) * 0.05)
        atendimento = "Ruim"
    elif 0 < qualidade < 10 and 0 < serviço < 10:

        valor_gorjeta = locale.currency(
            float(str(sistema_gorjeta.output['gorjeta']).replace('R$', '').replace(',', '.')) * 0.1)
        atendimento = "Regular"


    elif qualidade == 10 and serviço == 10:
        valor_gorjeta = locale.currency(
            float(str(sistema_gorjeta.output['gorjeta']).replace('R$', '').replace(',', '.')) * 0.15)
        atendimento = "Ótimo"
    print("A sua gorjeta  foi de {} ".format(valor_gorjeta, atendimento))
    # Quebra o loop
    opção = input("Deseja continuar? (S/N) ")
    if opção not in "Ss":
        break

# Encerra o programa
if atendimento == "Ótimo":
    print(("\U0001F6F6") * 10, "Obrigado por ter escolhido nosso restaurante para almoçar o  Bar do Mauro Gil!!!",
          ("\U0001F6F6") * 10)
    print(("\U0001F6F6") * 10, "Indique a conhecidos e que beleza", ("\U0001F6F6") * 10)
elif atendimento == "Regular":
    print(("\U0001F6F6") * 10, "Obrigado por ter escolhido nosso restaurante   para almoçar  o  Bar do Mauro Gil!!!",
          ("\U0001F6F6") * 10)

    print(("\U0001F6F6") * 10, "Volte,Sempre e que beleza", ("\U0001F6F6") * 10)
elif atendimento == "Ruim":
    print(("\U0001F6F6") * 10, "Obrigado por ter escolhido nosso restaurante   para almoçar  Bar do Mauro Gil!!!",
          ("\U0001F6F6") * 10)

    print(("\U0001F6F6") * 10, "Iremos melhorar  e que beleza", ("\U0001F6F6") * 10)
else:
    print("Digite novamente as opções que digitou  são inválidas!!!!")
