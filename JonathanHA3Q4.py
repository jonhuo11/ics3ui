# PConc A3Q4
# ICS3UI-01, Ms Harris
# Jonathan H
# Began: Nov 2, 2019
# Finished : Nov 6, 2019

'''
Create something recursive. Create a flowchart and IPO chart, very clearly
identify your base case. You may not use the Koch snowflake, or the Tower of
Hanoi. If you are stuck I suggest a palindrome checker.
'''

# I am going to code the fibonacci series and print it out
# As an extension I will use a dynamic programming technique to reduce running times
# Essentially I am storing values from previous recursive calls in a table
# Later recursive calls can get values from this table instead of double calling

# Dictionary of n values and corresponding outputs
n_table = {}

# Recursive fibonacci function
# Finds the nth fibonacci number
def fibonacci(n):
    # Use the global n_table which is outside scope
    global n_table

    # If f(n) has already been computed, then simply get the value
    if n in n_table:
        return n
    # If f(n) is not computed
    else:
        # Base cases
        # If n == 0 then the 0th fibonacci number is 0
        if n == 0:
            return 0 
        # The first 2 fibonacci numbers are 1 and 2
        elif n == 1 or n == 2:
            return 1

        # If none of the above is true, then we know f(n) = f(n-1) + f(n-2)
        # Keep reducing n value until we get to base case, then propagate the result upwards
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

# asks for user input, make sure you enter an integer
print("This program finds the Nth fibonacci number.")
print(fibonacci(int(input("Enter the N value: "))))
