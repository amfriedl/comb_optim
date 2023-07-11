import numpy as np

filename = "E:/Knapsack/Knap_C5I10.dat"  # Substitua pelo nome do arquivo real

# Variáveis para armazenar os dados lidos
linha = None
coluna = None
cost = None
rhs = None
matrix = None

# Função auxiliar para converter uma linha de valores em uma lista de floats
def parse_values(line):
    return [float(value) for value in line.strip().split()]

# Ler o arquivo e extrair os dados
with open(filename, "r") as file:
    lines = file.readlines()

# Ler o escalar
linha = int(lines[0].strip())
coluna = int(lines[2].strip())

# Ler o vetor
cost = np.array(parse_values(lines[5]))

# Ler a matriz
end = 7+ linha
matrix_lines = [line.strip() for line in lines[7:end]]
matrix = np.array([parse_values(line) for line in matrix_lines],dtype=object)

# Ler vetor de RHS
rhs = np.array(parse_values(lines[end+1]))

# Imprimir os dados lidos
print("linhas:", linha)
print("colunas:", coluna)
#print("cost:", cost)
#print("rhs:", rhs)
#print("Matrix:")
#for row in matrix:
#print(row)


#Criando uma matriz n x 2 que contém as médias das proporções custo/valor em ordem decrescente,
#seguidas da posição do respectivo objeto

ratios = np.zeros((coluna,2))

aux = np.array(matrix.sum(axis = 0)/linha)

for i in range(coluna):
    ratios[i,0] = aux[i]
    ratios[i,1] = i

ratios = ratios[np.lexsort(np.fliplr(ratios).T)]

ratios = np.flipud(ratios)

#print("Razões/Índices:",ratios)

#iniciando o vetor solução vazio
sol = np.zeros(coluna)

#Vetor para armazenar a soma dos custos
custos = np.zeros(linha)

#A cada item, verificamos se é possível colocá-lo na mochila. Se for, o colocamos, e atualizamos o custo total atual
for i in range(coluna):
    if all(custos + matrix[:,int(ratios[i,1])] <= rhs):
        sol[int(ratios[i,1])]=1
        custos = custos + matrix[:,int(ratios[i,1])]
        
print("Solução encontrada:",sol)
#print("Custo:",custos)
print("Valor:", sol.dot(cost))
if all(custos<=rhs):
    print("A solução construída é factível.")
else:
    print("A solução construída não é factível.")

#Realização de Swaps para obtenção de uma vizihança com potenciais soluções melhores

best_valor = sol.dot(cost)
custo_temp = matrix.dot(sol)
valor_temp = best_valor.copy()

for i in range(coluna):
    sol_temp = sol.copy()
    for j in range(coluna):
        #print(i,j)
        if i > j and sol_temp[i] != sol_temp[j]:
            temp = sol_temp[i].copy()
            sol_temp[i] = sol_temp[j].copy()
            sol_temp[j] = temp.copy()
            custo_temp = matrix.dot(sol_temp)
            valor_temp = sol_temp.dot(cost)
            if all(custo_temp <= rhs) and valor_temp > best_valor:
                best_sol = sol_temp.copy()
                bestbest_or = valor_temp.copy()

print("Após Swaps, a melhor solução encontrada foi:", best_sol)
#print("Custo:",matrix.dot(best_sol))
print("Valor:", best_sol.dot(cost))
if all(matrix.dot(best_sol)<=rhs):
    print("A nova solução construída é factível.")
else:
    print("A nova solução construída não é factível.")
