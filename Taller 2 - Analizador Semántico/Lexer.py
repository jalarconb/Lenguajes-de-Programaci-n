# -------------------------------------------------------------------------------------------------
# TODO:
# - Nada, ya pasé todos los casos <:
# -------------------------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------------------------

# FUNCIONES

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

# ------------------------------------------------------------------------------------------------

# INICIO DEL ANALIZADOR LÉXICO

		try:

			# NÚMEROS
			if getType(lineStrip) == 'NUMERO':
				id = getString(lineStrip, 'NUMERO')
				buffer = lineStrip.replace(id, '', 1)

				if line.count(lineStrip) > 1:
					index = line.index(lineStrip)
					# Subclasificación de tokens: Si hay parte decimal, se usa tkn_float; tkn_integer en otro caso
					if	"." in id:
						print(f'<tkn_float,{id},{fila},{line.index(lineStrip, index+1)+1}>')
					else:
						print(f'<tkn_integer,{id},{fila},{line.index(lineStrip, index+1)+1}>')
				else:
					# Subclasificación de tokens: Si hay parte decimal, se usa tkn_float; tkn_integer en otro caso
					if	"." in id:
						print(f'<tkn_float,{id},{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					else:
						print(f'<tkn_integer,{id},{fila},{line.index(lineStrip)+1}>')



			# IDENTIFICADORES
			elif getType(lineStrip) == 'ID':
				id = getString(lineStrip, 'ID')
				buffer = lineStrip.replace(id, '', 1)

				# Verificar si el ID es una palabra reservada
				if id in reservadas:
					if line.count(lineStrip) > 1:
						if lineStrip == id:
							print(f'<{id},{fila},{line.index(lineStrip, len(line)-len(id)-1)+1}>')
						else:
							index = line.index(lineStrip)
							print(f'<{id},{fila},{line.index(lineStrip, index+1)+1}>')
					elif line.index(buffer) == 0:
						print(f'<{id},{fila},{line.index(lineStrip)+1}>')
					else: 
						print(f'<{id},{fila},{line.index(lineStrip)+1}>')
				else:
					if lineStrip == id:
						print(f'<id,{id},{fila},{line.index(lineStrip, len(line)-len(id)-1)+1}>')
					elif line.count(lineStrip) > 1:
						index = line.index(lineStrip)
						print(f'<id,{id}, {fila},{line.index(lineStrip, index+1)+1}>')
					else:
						print(f'<id,{id},{fila},{line.index(lineStrip)+1}>')

			# OPERADORES
			elif getType(lineStrip) == 'OPERADORES':
				id = getString(lineStrip, 'OPERADORES')
				buffer = lineStrip.replace(id, '', 1)
				
				# Operadores de dos símbolos: ==, >=, <=, !=
				if (id == '=' or id == '<' or id == '>' or id == '!') and buffer != '' and buffer[0] == '=':
					id += '='
					buffer = buffer[1:]

					if id == '==':
						print(f'<tkn_equal,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					elif id == '<=':
						print(f'<tkn_leq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					elif id == '>=':
						print(f'<tkn_geq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
					elif id == '!=':
						print(f'<tkn_neq,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')

				# Operadores de un símbolo
				elif id == '=':
					print(f'<tkn_assign,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '<':
					print(f'<tkn_less,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '>':
					print(f'<tkn_greater,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '+':
					print(f'<tkn_plus,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '-':
					print(f'<tkn_minus,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '/':
					print(f'<tkn_div,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '*':
					print(f'<tkn_times,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '%':
					print(f'<tkn_mod,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '?':
					print(f'<tkn_question_mark,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				elif id == '!':
					# El operador "!" por sí solo no existe, solo aparece en "!="
					print(f'>>> Error lexico (linea: {fila}, posicion: {len(staticLineStrip)-len(lineStrip)+1})')
					exit()

			# SÍMBOLOS
			elif getType(lineStrip) == 'SIMBOLOS':
				id = getString(lineStrip, 'SIMBOLOS')
				buffer = lineStrip.replace(id, '', 1)

				if id == '(':
					print(f'<tkn_opening_par,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == ',':
					print(f'<tkn_comma,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == ')':
					print(f'<tkn_closing_par,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == ']':
					print(f'<tkn_closing_bra,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == '[':
					print(f'<tkn_opening_bra,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == ';':
					print(f'<tkn_semicolon,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')
				if id == '.':
					print(f'<tkn_period,{fila},{len(staticLineStrip)-len(lineStrip)+1}>')

			

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
						
						print(f'<tkn_str,{id[1:len(id)-1]},{fila},{len(staticLineStrip)-len(lineStrip)+1}>')

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

	fila += 1