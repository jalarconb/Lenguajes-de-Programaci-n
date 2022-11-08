# // Arreglos en CORAL

# integer array(?) userNums
# float array(5) userVals

# float x
# float y
# integer i

# userNums.size = 5

# for i = 0; i < userNums.size; i = i + 1
#    userNums[i] = i * 2
#    userVals[4-i] = (4*i)/2

# x = userNums[3]
# y = userVals[3]

# for i = 0; i < userNums.size; i = i + 1
#    Put   userNums[i]    -  x+y     to   output

# --------------------------------------------------------------------------

# Arreglos en CORAL

userNums = [0]

userVals = [0.0] * 5

x: float
y: float
i: int

# userNums.size = 5
for i in range(-1,5):
    userNums.append(userNums[0])

for i in range(0, len(userNums), 1):
    userNums[i] = i*2
    userVals[4-i] = (4*i/2)

x = userNums[3]
y = userVals[3]

for i in range(0, len(userNums), 1):
    print(userNums[i]    -  x+y, end='')