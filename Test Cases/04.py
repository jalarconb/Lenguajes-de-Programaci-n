# Function factorial_recursive(integer n) returns integer res
#    // Base case: 1! = 1
#    if (n == 1)
#       res = 1
      
#    // Recursive case: n! = n * (n-1)!
#    else
#       res = n * factorial_recursive(n-1)

# integer b

# Function Main() returns nothing
#    integer evaluates
#    evaluates = factorial_recursive(factorial_recursive(3))
#    Put evaluates to output

# -------------------------------------------------------------------

def factorial_recursive(n: int):
    # Base case: 1! = 1
    if (n == 1):
        res = 1

    # Recursive case: n! = n * (n-1)!
    else:
        res = n * factorial_recursive(n-1)
    
    return int(res)

def Main():
    evaluates: int
    evaluates = factorial_recursive(factorial_recursive(3))
    print(evaluates, end='')

Main()