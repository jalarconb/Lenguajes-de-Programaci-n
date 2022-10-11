# -------------------------------------------------------------------------------------------------
#                                 ANALIZADOR LÉXICO-SINTÁCTICO
# -------------------------------------------------------------------------------------------------
# Se hicieron midificaciones en el analizador léxico para facilitar el trabajo del analizador
# sintáctico.
# 
# TODO: Cambios realizados
# - La salida ya no se imprime sino que se guarda en una lista de tokens que sirve de input
# 	para el analizador sintáctico.
# - <id,linea,columna> (y otros similares) ahora salen <id,id,linea,columna>.
# -------------------------------------------------------------------------------------------------

# IMPORTS Y DECLARACIONES

import os
import re
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Palabras reservadas del lenguaje
reservadas = [
	'AbsoluteValue','and','array','decimal','else','elseif','float','for','Function','Get',
	'if','input','integer','Main','next','not','nothing','or','output','places','Put','RaiseToPower','RandomNumber','returns',
	'SeedRandomNumbers','SquareRoot','size','to','while','with',#'evaluates'
]

# Expresiones regulares: "Familias" de lexemas en el lenguaje
regEx = {
	'NUMERO': r'([-+]?[0-9]+(\.[0-9]+)?)',
	'COMENTARIO': r'([/]+[/]+.*)',
	'ID': r'([A-Za-z]+[0-9A-Za-z_]*)',
	'OPERADORES': r'([+\-*/>=<%!?])',
	'SIMBOLOS': r'([\,\]\[)(\.;])',
	# 'CADENA': r'([", \']{1})'
	'CADENA': r'(["]{1})'
}

# Inicio desde la primera fila
fila = 1

# Variables para almacenar el token actual
tknPop = []
tkn = ''
tknLex = ''
tknLine = ''
tknCol = ''

# Conjuntos de predicción de la gramática en formato diccionario (generados con refinePredict.py y grammar.txt)
termsDict = {'[S]0': ['integer', 'float'], '[S]1': ['Put'], '[type]0': ['integer'], '[type]1': ['float'], '[identifier]0': ['tkn_id'], '[item]0': ['tkn_id'], '[item]1': ['tkn_str'], '[item]2': ['[arithexpr]']}

instructDict = {'[S]0': ['type()', 'identifier()'], '[S]1': ["match('Put')", 'item()', "match('to')", "match('output')"], '[type]0': ["match('integer')"], '[type]1': ["match('float')"], '[identifier]0': ["match('tkn_id')"], '[item]0': ["match('tkn_id')"], '[item]1': ["match('tkn_str')"], '[item]2': ['arithexpr()']}

# ------------------------------------------------------------------------------------------------

# FUNCIONES LÉXICAS


# "Recorta" el patrón de la línea para trabajar con él
def getString(line, pattern):
	match = re.split(regEx[pattern], line)
	if len(match) == 1:
		return match[0]
	return match[1]

# Regresa el tipo de regEx de una subcadena de la línea
def getType(line):
	if re.compile(regEx['OPERADORES']).match(line):
		return 'OPERADORES'
	elif re.compile(regEx['NUMERO']).match(line):
		return 'NUMERO'
	elif re.compile(regEx['ID']).match(line):
		return 'ID'
	elif re.compile(regEx['OPERADORES']).match(line):
		return 'OPERADORES'
	elif re.compile(regEx['SIMBOLOS']).match(line):
		return 'SIMBOLOS'
	elif re.compile(regEx['CADENA']).match(line):
		return 'CADENA'

# Inicializa la línea
line = ' '
# Inicializa la cola de tokens y lexemas
tknList = []

# ------------------------------------------------------------------------------------------------

# FUNCIONES SINTÁCTICAS

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
	# print(f'\ntknPop: {tknPop}')

# Imprime Error Sintáctico
def sintError(found, expected, line, col):
	print(f'<{line}:{col}> Error sintactico: se encontro: <{found}>; se esperaba: <{translateTerms(expected)}>.')
	# os._exit(1)
	sys.exit()

# Revisa si el toquen recibido era el esperado
def match(tknEsperado):
	if tknEsperado == tkn:
		# print(f'\t---------- match() ----------\n\ttkn: {tkn}\n\ttknEsperado: {tknEsperado}')
		getNextToken()
		return
	else:
		# print(f'\t---------- match ERROR ----------')
		sintError(tkn,tknEsperado,tknLine,tknCol)


# ------------------------------------------------------------------------------------------------

# REGLAS GRAMATICALES

# Símbolo inicial de la gramática
def S():
	# print('-------------------- S() --------------------')	
	rule = 'S'
	x = 0
	try:
		# Recorre todas las reglas de S para ver si alguna aplica al tkn
		while True:
			# print(f'x = {x}')
			if tkn in termsDict[f'[{rule}]'+str(x)]:
				# print(instructDict[f'[{rule}]'+str(x)])
				# Ejecuta todas las instrucciones encontradas en la regla S[x]
				for i in range(0,len(instructDict['[S]'+str(x)])):
					eval(instructDict[f'[{rule}]'+str(x)][i])
				# print('breik')
				break;
			x += 1
	# Si ninguna aplica, es que no se esperaba ese tkn ---> error
	except KeyError:
		expectedString = ''
		for i in range(x-1,-1,-1):
			expectedString = expectedString + str(termsDict[f'[{rule}]'+str(i)])
		expectedString = expectedString.replace(' ','').replace('][',',').replace(',',', ').replace('\'','"')[1:len(expectedString)-1]
		# print('xd')
		sintError(tkn,expectedString,tknLine,tknCol)


def type():
	# print('-------------------- type() --------------------')
	match('integer')

def identifier():
	# print('----------------- identifier() -----------------')
	match('id')

def item():
	# print('-------------------- item() --------------------')
	match('id')


# -------------------------------------------------------------------------------------------------
# -------------------------------------- INICIO DEL PROGRAMA --------------------------------------
# -------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------

# INICIO DEL ANALIZADOR LÉXICO

while line:
	# Leer línea
	line = sys.stdin.readline()

	# Elimina espacios al inicio y al final de la línea
	lineStrip = line.strip()

	# Elimina los espacios al final de la línea
	staticLineStrip = line.rstrip()

	# Inicialización del Buffer y el ID
	#   lineStrip : ID + Buffer
	#   (ID tiene lo ya analizado, Buffer lo que queda)
	buffer = ''
	id = ''

	# Saltar líneas vacías
	if line == '\n':
		fila += 1
		continue
	
	# Saltar líneas de comentario "//"
	if re.compile(regEx['COMENTARIO']).match(lineStrip):
		fila += 1
		continue

	# Clasificar cada palabra en la cadena de entrada
	while buffer != '\n':
		
		# Saltar líneas rellenas solo de espacios
		if lineStrip == '':
			break
		
		if buffer != '':
			lineStrip = buffer.strip()
		
		index = line.index(lineStrip)

		# TODO: EN CASO DE QUE SE ACEPTARAN COMENTARIOS A MITAD DE LÍNEA:
		# Si de repente se encuentra un comentario a mitad de línea ---> saltar línea
		# if re.compile(regEx['COMENTARIO']).match(lineTemp):
		# 	break

		try:

			# NÚMEROS
			if getType(lineStrip) == 'NUMERO':
				id = getString(lineStrip, 'NUMERO')
				buffer = lineStrip.replace(id, '', 1)

				if line.count(lineStrip) > 1:
					index = line.index(lineStrip)
					# Subclasificación de tokens: Si hay parte decimal, se usa tkn_float; tkn_integer en otro caso
					if	"." in id:
						# print(f'<tkn_float,{id},{fila},{line.index(lineStrip, index+1)+1}>')
						tknList.append(['tkn_float',id,fila,len(staticLineStrip)-len(lineStrip)+1])
					else:
						# print(f'<tkn_integer,{id},{fila},{line.index(lineStrip, index+1)+1}>')
						tknList.append(['tkn_integer',id,fila,line.index(lineStrip)+1])
				else:
					# Subclasificación de tokens: Si hay parte decimal, se usa tkn_float; tkn_integer en otro caso
					if	"." in id:
						# print(f'<tkn_float,{id},{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_float',id,fila,len(staticLineStrip)-len(lineStrip)+1])
					else:
						# print(f'<tkn_integer,{id},{fila},{line.index(lineStrip)+1}>')
						tknList.append(['tkn_integer',id,fila,line.index(lineStrip)+1])



			# IDENTIFICADORES
			elif getType(lineStrip) == 'ID':
				id = getString(lineStrip, 'ID')
				buffer = lineStrip.replace(id, '', 1)

				# Verificar si el ID es una palabra reservada
				if id in reservadas:
					if line.count(lineStrip) > 1:
						if lineStrip == id:
							# print(f'<{id},{fila},{line.index(lineStrip, len(line)-len(id)-1)+1}>')
							tknList.append([id,id,fila,line.index(lineStrip, len(line)-len(id)-1)+1])
						else:
							index = line.index(lineStrip)
							# print(f'<{id},{fila},{line.index(lineStrip, index+1)+1}>')
							tknList.append([id,id,fila,line.index(lineStrip, index+1)+1])
					elif line.index(buffer) == 0:
						# print(f'<{id},{fila},{line.index(lineStrip)+1}>')
						tknList.append([id,id,fila,line.index(lineStrip)+1])
					else: 
						# print(f'<{id},{fila},{line.index(lineStrip)+1}>')
						tknList.append([id,id,fila,line.index(lineStrip)+1])
				else:
					if lineStrip == id:
						# print(f'<id,{id},{fila},{line.index(lineStrip, len(line)-len(id)-1)+1}>')
						tknList.append(['id',id,fila,line.index(lineStrip, len(line)-len(id)-1)+1])
					elif line.count(lineStrip) > 1:
						index = line.index(lineStrip)
						# print(f'<id,{id}, {fila},{line.index(lineStrip, index+1)+1}>')
						tknList.append(['id',id,fila,line.index(lineStrip, index+1)+1])
					else:
						# print(f'<id,{id},{fila},{line.index(lineStrip)+1}>')
						tknList.append(['id',id,fila,line.index(lineStrip)+1])

			# OPERADORES
			elif getType(lineStrip) == 'OPERADORES':
				id = getString(lineStrip, 'OPERADORES')
				buffer = lineStrip.replace(id, '', 1)
				
				# Operadores de dos símbolos: ==, >=, <=, !=
				if (id == '=' or id == '<' or id == '>' or id == '!') and buffer != '' and buffer[0] == '=':
					id += '='
					buffer = buffer[1:]

					if id == '==':
						# print(f'<tkn_equal,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_equal',id,fila,len(staticLineStrip)-len(lineStrip)+1])
					elif id == '<=':
						# print(f'<tkn_leq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_leq',id,fila,len(staticLineStrip)-len(lineStrip)+1])
					elif id == '>=':
						# print(f'<tkn_geq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_geq',id,fila,len(staticLineStrip)-len(lineStrip)+1])
					elif id == '!=':
						# print(f'<tkn_neq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_neq',id,fila,len(staticLineStrip)-len(lineStrip)+1])

				# Operadores de un símbolo
				elif id == '=':
					# print(f'<tkn_assign,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_assign',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '<':
					# print(f'<tkn_less,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_less',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '>':
					# print(f'<tkn_greater,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_greater',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '+':
					# print(f'<tkn_plus,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_plus',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '-':
					# print(f'<tkn_minus,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_minus',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '/':
					# print(f'<tkn_div,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_div',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '*':
					# print(f'<tkn_times,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_times',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '%':
					# print(f'<tkn_mod,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_mod',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '?':
					# print(f'<tkn_question_mark,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_question_mark',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				elif id == '!':
					# El operador "!" por sí solo no existe, solo aparece en "!="
					print(f'>>> Error lexico (linea: {fila}, posicion: {len(staticLineStrip)-len(lineStrip)+1})')
					exit()

			# SÍMBOLOS
			elif getType(lineStrip) == 'SIMBOLOS':
				id = getString(lineStrip, 'SIMBOLOS')
				buffer = lineStrip.replace(id, '', 1)

				if id == '(':
					# print(f'<tkn_opening_par,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_opening_par',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == ',':
					# print(f'<tkn_comma,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_comma',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == ')':
					# print(f'<tkn_closing_par,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_closing_par',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == ']':
					# print(f'<tkn_closing_bra,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_closing_bra',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == '[':
					# print(f'<tkn_opening_bra,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_opening_bra',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == ';':
					# print(f'<tkn_semicolon,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_semicolon',id,fila,len(staticLineStrip)-len(lineStrip)+1])
				if id == '.':
					# print(f'<tkn_period,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					tknList.append(['tkn_period',id,fila,len(staticLineStrip)-len(lineStrip)+1])

			

			# CADENAS
			elif getType(lineStrip) == 'CADENA':
				id = getString(lineStrip, 'CADENA')
				buffer = lineStrip.replace(id, '', 1)

				try:
					if id == '"':
						# CASO 1: Hay \" en el Buffer
						while '\\"' in buffer:

							# Revisa las posiciones de la próxima " y el próximo \"
							indexComilla = buffer.index('"')
							indexBarraComilla = buffer.index('\\"')

							# CASO 1.1: El \" es inmediato y NO DEBE cortar la cadena
							if indexComilla == (indexBarraComilla + 1):
								index = indexComilla
								id = id + buffer[:index+1]
								buffer = buffer[index+1:]
							# CASO 1.2: El \" NO es inmediato, se puede ignorar por ahora
							else:
								index = buffer.index('"')
								id = id + buffer[:index+1]
								buffer = buffer[index+1:]
								break
						# CASO 2: No hay \" en el Buffer
						else:
							index = buffer.index('"')
							id = id + buffer[:index+1]
							buffer = buffer[index+1:]
						
						# print(f'<tkn_str,{id[1:len(id)-1]},{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
						tknList.append(['tkn_str',id[1:len(id)-1],fila,len(staticLineStrip)-len(lineStrip)+1])

				except ValueError:
					# Error léxico: No se logró cerrar la cadena
					print(f'>>> Error lexico (linea: {fila}, posicion: {len(staticLineStrip)-len(lineStrip)+1})')
					exit()

			# Error léxico DEFAULT
			elif lineStrip != None and id != '\n':
				print(f'>>> Error lexico (linea: {fila}, posicion: {len(staticLineStrip)-len(lineStrip)+1})')
				exit()

		except (IndexError) as e:
			pass

		# Buffer vacío equivale a línea nueva (skip)
		if buffer == '':
			buffer = '\n'		

	tknList.append(['tkn_eol','$',fila,len(staticLineStrip)-len(lineStrip)+1])

	fila += 1

tknList.append(['tkn_eof','EOF',fila,len(staticLineStrip)-len(lineStrip)+1])
# print(tknList)
	
# ------------------------------------------------------------------------------------------------

# INICIO DEL ANALIZADOR SINTÁCTICO
	
# print(f'\ntknList: {tknList}')

# Análisis sintáctico mientras aún haya elementos en la tknList
while len(tknList) > 0:
	# print('\n============================= CICLO PRINCIPAAAAAAAAAAAAAAAAAL =============================')
	getNextToken()
	if tkn == 'tkn_eol':
		getNextToken()
		continue
	if tkn == 'tkn_eof' and len(tknList) == 1:
		break
	S()

# if tkn != '$':
#   print('error: $')

# print('')
print("El analisis sintactico ha finalizado exitosamente.")
# print('')