from additionals import *
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']

def ceaser_ciphar(message, shift, code_type):
    ceaser_ciphar = ''
    if code_type == 'decode':
        shift *= -1
    for char in message:
        if not char.isalpha():
            ceaser_ciphar += char
        else:
            new_index = alphabet.index(char) + shift
            ceaser_ciphar += alphabet[new_index]
    print(f"The {code_type.title()} message : {ceaser_ciphar}")

def inp():
    message = input("Type your message : \n").lower()
    shift = int(input("Enter Shift Number : \n"))
    if shift > 26:
        shift %= 26
    return message, shift

def check():
    user = input("Would you like to do more? Type 'Yes' or 'No' \n").lower()
    if user == 'yes':
        return True
    elif user == 'no':
        return False
    else:
        print("Wrong Option")
        return False

flag = True

while flag:
    print(logo)
    code_type = input("Type 'encode' for Encryption and 'decode' for Decryption or 'exit' to quit : \n").lower()

    if code_type in ['encode', 'decode']:
        message, shift = inp()
        ceaser_ciphar(message,shift,code_type)
        flag = check()
    elif code_type == 'exit':
        flag = False
    else:
        print(f"Invalid Input , Try again....")

print("System Terminated")