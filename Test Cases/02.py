# // Triángulo de Pascal

# integer rows
# integer coef
# integer space
# integer i
# integer j

# rows = 8

# for i = 0; i < rows; i = i + 1

#    for space = 1; space <= rows-i; space = space + 1
#       Put "  " to output
      
#    for j = 0; j <= i; j = j + 1
   
#       if j==0 or i==0
#          coef = 1
#       else
#          coef = coef*(i-j+1)/j
      
#       Put coef to output
#       Put "   " to output
   
#    Put "\n" to output

# ---------------------------------------------------------------------------

# Triángulo de Pascal

coef: int
rows: int
space: int
i: int
j: int

rows = 8

for i in range(0,rows,1):

  for space in range(1,rows-i+1,1):
      print("  ", end='')

  for j in range(0,i+1,1):

    if j==0 or i==0:
      coef = 1
    else:
      coef = coef*(i-j+1)/j

    print(coef, end='')
    print("   ", end='')

  print("\n", end='')