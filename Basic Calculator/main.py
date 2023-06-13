def add(x,y):
    return x+y

def substract(x,y):
    return x-y

def multiply(x,y):
    return x*y

def divide(x,y):
    return x/y

operators = ["+","-","*","/"]
more = 'yes'

while more == 'yes':
    result = float(input("What's Your First Number?  "))
    cont = 'y'
    while cont == 'y':

        num1 = result
        for operator in operators:
            print(operator)

        operation = input("Pick an Operator: ")
        num2 = float(input("What's Your 2nd Number? "))

        if operation == "+":
            result = add(num1, num2)
            print(f"{num1} {operation} {num2} = {result}")
        elif operation == "-":
            result = substract(num1, num2)
            print(f"{num1} {operation} {num2} = {result}")
        elif operation == "*":
            result = multiply(num1, num2)
            print(f"{num1} {operation} {num2} = {result}")
        elif operation == "/":
            result = divide(num1, num2)
            print(f"{num1} {operation} {num2} = {result}")
        else:
            print("Wrong operator,pick an operation from above!")
        cont = input(f"Type 'y' to continue calculating with {result} or Type 'n' for new calculation ").lower()

    more = input("Do you want to perform more calculations? Type 'yes' or 'no' : ").lower()

print("Good Bye")