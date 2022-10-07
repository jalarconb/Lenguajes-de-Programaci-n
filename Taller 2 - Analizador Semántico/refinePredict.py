# -------------------------------------------------------------------------------------------------
# REFINADOR DEL CONJUNTO DE PREDICCIÓN DE GRAMÁTICAS
# 
# Este código cambia el formato de las líneas del conjunto de predicción:
#       antes:  A ->  B C : big bet
#       ahora: 'A0': ['big', 'bet']
# Las nuevas reglas se guardan en formato diccionario, para usarse en el Analizador Sintáctico
# -------------------------------------------------------------------------------------------------

import sys

# Conjunto de predicción refinado
predict = {}

# No terminal actual. Aquí se pone el primero de la gramática
currentNonTerm = 'A'

# Subíndice del no terminal actual, en caso de haber varias reglas
x = 0

# Lee las líneas del archivo de conjuntos de predicción
with open('predictionSet.txt', 'r') as file:
    lines = file.readlines()

# Elimina las líneas vacías
try:
    while True:
        lines.remove('\n')
except ValueError:
    pass

# La cantidad de líneas es el número de iteraciones para el siguiente for
linesLength = len(lines)

for i in range(0,linesLength):

  # Recoge la primera línea para tratarla
  line = lines.pop(0)

  # Guarda el no terminal de la regla
  nonTerm = line[0]

  # Si es un nuevo no terminal, reinicia el subíndice x
  if currentNonTerm != nonTerm:
    x = 0
    currentNonTerm = nonTerm
  
  # Concatena el no terminal con el subíndice
  nonTerm = nonTerm + str(x)
  x += 1

  # Guarda la parte de la línea que tiene los terminales y los separa
  term = line[line.index(':')+1:len(line)]
  term = term.strip().split(' ')

  # Agrega la regla al diccionario de predicción
  predict[nonTerm] = term

with open('predictionSetRefined.txt', 'w') as file:
  sys.stdout = file
  print(predict)