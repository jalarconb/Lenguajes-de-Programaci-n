# -------------------------------------------------------------------------------------------------
# REFINADOR DEL CONJUNTO DE PREDICCIÓN DE GRAMÁTICAS
# 
# Este código cambia el formato de las líneas del conjunto de predicción:
#       antes:  A ->  B C : big bet
#       ahora: 'A0': ['big', 'bet']
# Las nuevas reglas se guardan en formato diccionario, para usarse en el Analizador Sintáctico
# -------------------------------------------------------------------------------------------------

import sys

# Diccionarios refinados: Términos e Instrucciones
termsDict = {}
instructDict = {}

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


# lines de prueba
# lines = ['[S] ->  [type] [identifier] : integer float']


# La cantidad de líneas es el número de iteraciones para el siguiente for
linesLength = len(lines)

for i in range(0,linesLength):

  # Recoge la primera línea para tratarla
  line = lines.pop(0)

  # Guarda el no terminal de la regla
  nonTerm = line[0:line.index('-')-1]

  # Si es un nuevo no terminal, reinicia el subíndice x
  if currentNonTerm != nonTerm:
    x = 0
    currentNonTerm = nonTerm
  
  # Concatena el no terminal con el subíndice
  nonTerm = nonTerm + str(x)
  x += 1

  # Guarda la parte de la línea que tiene las instrucciones y las separa
  instruct = line[line.index('-')+2:line.index(':')]
  instruct = instruct.strip()
  # print(f'instruct: {instruct}')
  instruct = instruct.split(' ')
  # print(f'instruct Split: {instruct}')

  # Reemplaza los term por match('term') y los [no-term] por no-term()
  for j in range(0,len(instruct)):
    # No terminal
    if instruct[j][0] == '[' and instruct[j][len(instruct[j])-1] == ']':
      instruct[j] = instruct[j].lstrip('[').rstrip(']') + '()'
    # Terminal
    else:
      instruct[j] = 'match(\'' + instruct[j] + '\')'
  
  # Guarda la parte de la línea que tiene los terminales y los separa
  term = line[line.index(':')+1:len(line)]
  term = term.strip().split(' ')

  # Agrega la regla al diccionario de predicción
  instructDict[nonTerm] = instruct
  termsDict[nonTerm] = term

with open('predictionSetRefined.txt', 'w') as file:
  sys.stdout = file
  print(f'termsDict = {termsDict}\n\ninstructDict = {instructDict}')