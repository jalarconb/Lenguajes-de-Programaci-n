# // Loops & Branches

# float x
# integer i
# float xSquared

# x = RandomNumber(-10,10)
# Put "El número escogido fue:" to output
# Put x to output
# Put "\n" to output

# if x >= 1
#    // Print x^2 desc
#    while x > 0
#       xSquared = x * x
#       Put xSquared to output with 3 decimal places
#       Put "\n" to output
#       x = x - 1
# elseif x == 0
#    // Print "0.00000000"
#    Put x to output with 8 decimal places
# else
#    // Count even numbers down from 10 to 0
#    for i = 10; i >= 0; i = i - 2
#       Put i to output with 2 decimal places
#       // Add 10-i spaces between numbers
#       x = i
#       while (x < 12)
#          Put " " to output
#          x = x + 2

# ----------------------------------------------------------------------------------------------

# Loops & Branches

x: float
i: int
xSquared: float

# x = RandomNumber(-10,10)
x = 7

print("El número escogido fue:", end='')
print(x, end='')
print("\n", end='')

if x >= 1:
    # Print x^2 desc
    while x > 0:
        xSquared = x * x
        # Put xSquared to output with 3 decimal places
        print(round(xSquared,3), end='')
        print("\n", end='')
        x = x - 1
elif x == 0:
    # Print "0.00000000"
    print(round(x,8), end='')
else:
    # Count even numbers down from 10 to 0
    for i in range(10,0-1,-2):
        print(round(i,2), end='')
        # Add 10-i spaces between numbers
        x = i
        while (x < 12):
            print(" ", end='')
            x = x + 2