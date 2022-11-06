# integer b
# integer h
# float rectangle_area
# float triangle_area

# b = 15
# h = 11

# rectangle_area = b*h
# triangle_area = rectangle_area/2

# Put rectangle_area to output
# Put "\n-----\n" to output
# Put triangle_area to output

# ------------------------------------------
# TODO:
# - Revisar tipos de datos para que sean menos dinámicos.
# ------------------------------------------

b: int
h: int
rectangle_area: float
triangle_area: float

b = 15
h = 11

rectangle_area = b*h
triangle_area = rectangle_area/2

print(rectangle_area, end='')
print("\n-----\n", end='')
print(triangle_area, end='')