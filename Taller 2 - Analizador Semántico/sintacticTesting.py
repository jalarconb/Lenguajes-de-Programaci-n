# -------------------------------------------------------------------------------------------------
# TODO:
# - Este código ya analiza reglas gramaticales de una línea. Falta completar la gramática.
# - Implementar métodos para analizar estructuras de varias líneas
# -------------------------------------------------------------------------------------------------

import os
import sys

# Variables para almacenar el token actual
tknPop = []
tkn = ''
tknLex = ''
tknLine = ''
tknCol = ''

tknList = [['integer', 'integer', 1, 1], ['id', 'holaxd', 1, 9], ['tkn_eol', '$', 1, 9], ['Put', 'Put', 2, 1], ['id', 'x', 2, 5], ['to', 'to', 2, 7], ['output', 'output', 2, 10], ['tkn_eol', '$', 2, 10], ['tkn_eol', '$', 3, 1], ['tkn_eof', 'EOF', 4, 1]]

termsDict = {'[S]0': ['integer', 'float'], '[S]1': ['Put'], '[type]0': ['integer'], '[type]1': ['float'], '[identifier]0': ['tkn_id'], '[item]0': ['tkn_id'], '[item]1': ['tkn_str'], '[item]2': ['[arithexpr]']}

instructDict = {'[S]0': ['type()', 'identifier()'], '[S]1': ["match('Put')", 'item()', "match('to')", "match('output')"], '[type]0': ["match('integer')"], '[type]1': ["match('float')"], '[identifier]0': ["match('tkn_id')"], '[item]0': ["match('tkn_id')"], '[item]1': ["match('tkn_str')"], '[item]2': ['arithexpr()']}

# -------------------------------------------------------------------------------------
# ------------------------------ DEFINICIÓN DE FUNCIONES ------------------------------
# -------------------------------------------------------------------------------------

# Convierte los términos de los tokens por la nueva salida solicitada
def translateTerms(string):
	# print(string)
	string = string.replace('tkn_integer','integer_value')
	string = string.replace('tkn_float','float_value')
	string = string.replace('tkn_str','string_literal')
	string = string.replace('tkn_str','string_literal')
	return string

# Recoge el siguiente token (Que es el primer elemento de tknList)
def getNextToken():
	global tknPop, tkn, tknLex, tknLine, tknCol
	tknPop = tknList.pop(0)
	tkn = tknPop[0]
	tknLex = tknPop[1]
	tknLine = tknPop[2]
	tknCol = tknPop[3]
	print(f'\ntknPop: {tknPop}')

# Imprime Error Sintáctico
def sintError(found, expected, line, col):
	print(f'<{line}:{col}> Error sintactico: se encontro: <{found}>; se esperaba: <{translateTerms(expected)}>.')
	# os._exit(1)
	sys.exit()

# Revisa si el toquen recibido era el esperado
def match(tknEsperado):
	if tknEsperado == tkn:
		print(f'\t---------- match() ----------\n\ttkn: {tkn}\n\ttknEsperado: {tknEsperado}')
		getNextToken()
		return
	else:
		print(f'\t---------- match ERROR ----------')
		sintError(tkn,tknEsperado,tknLine,tknCol)

# -------------------------------------------------------------------------------------
# REGLAS GRAMATICALES

# Símbolo inicial de la gramática
def S():
	print('-------------------- S() --------------------')	
	rule = 'S'
	x = 0
	try:
		# Recorre todas las reglas de S para ver si alguna aplica al tkn
		while True:
			# print(f'x = {x}')
			if tkn in termsDict[f'[{rule}]'+str(x)]:
				print(instructDict[f'[{rule}]'+str(x)])
				# Ejecuta todas las instrucciones encontradas en la regla S[x]
				for i in range(0,len(instructDict['[S]'+str(x)])):
					eval(instructDict[f'[{rule}]'+str(x)][i])
				print('breik')
				break;
			x += 1
	# Si ninguna aplica, es que no se esperaba ese tkn ---> error
	except KeyError:
		expectedString = ''
		for i in range(x-1,-1,-1):
			expectedString = expectedString + str(termsDict[f'[{rule}]'+str(i)])
		expectedString = expectedString.replace(' ','').replace('][',',').replace(',',', ').replace('\'','"')[1:len(expectedString)-1]
		print('xd')
		sintError(tkn,expectedString,tknLine,tknCol)


def type():
	print('-------------------- type() --------------------')
	match('integer')

def identifier():
	print('----------------- identifier() -----------------')
	match('id')

def item():
	print('-------------------- item() --------------------')
	match('id')

# -------------------------------------------------------------------------------------
# -------------------------------- INICIO DEL PROGRAMA --------------------------------
# -------------------------------------------------------------------------------------

print(f'\ntknList: {tknList}')

# Análisis sintáctico mientras aún haya elementos en la tknList
while len(tknList) > 0:
	print('\n============================= CICLO PRINCIPAAAAAAAAAAAAAAAAAL =============================')
	getNextToken()
	if tkn == 'tkn_eol':
		getNextToken()
		continue
	if tkn == 'tkn_eof' and len(tknList) == 1:
		break
	S()

# if tkn != '$':
#   print('error: $')

print('')
print("El analisis sintactico ha finalizado exitosamente.")
print('')