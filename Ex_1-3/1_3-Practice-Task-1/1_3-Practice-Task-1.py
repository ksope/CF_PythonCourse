a = int(input("Enter a number: "))
b = int(input("Enter another number to be added to the first: "))
c = int(input("Enter another number again to be added to the second: "))
operatorSign = input("Enter + to add the numbers or - to subtract the numbers: ")

if operatorSign == '+':
    print("The sum of these numbers is " + str(a + b + c))
elif operatorSign == '-':
    print("The sum of these numbers is " + str(a - b - c))
else:
    print('You will need to enter a "+" sign or "-" sign')