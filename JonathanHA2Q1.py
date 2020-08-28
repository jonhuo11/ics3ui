# ICS3UI-01 for Ms. Harris
# PConc A2Q#1
# Jonathan Huo
# Began: Sept 25, 2019
# Finished: Sept 25, 2019
'''
Create a flowchart, then write a program to perform a unit conversion of
your own choosing. Make sure that the program prints an introduction that explains what it
does. User output is important for understanding. Typical conversions are temperature,
measurements, speed, etc. meet level 3 curriculum expectations.
'''

# Output a short description of what the program does (convert between celsius/fahrenheit)
print("This program converts temperature values between celsius and fahrenheit.")

# Ask the user which unit they want to convert to, this is for a level 4 solution
do_celsius = input("Do you want to convert to celsius or fahrenheit? (Type C or F) ")

# Variable to store the suffix to add depending on which unit the user selects
suffix = ""
# If the user types C, set do_celsius to True
if (do_celsius == "C"):
    do_celsius = True
    # This suffix is used later on to improve output
    suffix = "celsius"
# If the user types F, set do_celsius to False
elif (do_celsius == "F"):
    do_celsius = False
    suffix = "fahrenheit"
# If there is an incorrect input, default to celsius = True
else:
    print("User did not input C or F, the program will convert to celsius by default.")
    do_celsius = True
    suffix = "celsius"

# Ask the user to input a temperature value, converting it to an int as well
temp = int(input("Enter the temperature you wish to convert from: "))

# If do_celsius = True, then convert the number from fahrenheit to celsius
if (do_celsius):
    # Math to convert units, rounding to the 2nd decimal point
    converted = round((temp - 32) * (5/9), 2)
# Otherwise if do_celsius = False, then convert to fahrenheit
else:
    # Math to convert units, rounding to the 2nd decimal point
    converted = round((temp * (9/5)) + 32, 2)

# Output the converted number, adding the suffix which depends on original user input
print("Your converted temperature is " + str(converted) + " degrees " + suffix + ".")
