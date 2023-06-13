from additionals import *

CASH_STATEMENTS = {"How many Quarters?: ": 0.25, "How many dimes?: ": 0.1, "How many Nickles?: ": 0.05,
                   "How many Pennies?: ": 0.01}
money = 0


def display_report():
    for resource, unit in zip(resources, ['ml', 'ml', 'gram']):
        print(f"{resource.title()} : {resources[resource]} {unit}")
    print(f"Money: ${money}")


def check_ingredients(opt):
    flag = True
    for ingredient, resource in zip(MENU[opt]['ingredients'], resources):
        menu_ele = MENU[opt]['ingredients'][ingredient]
        resource_ele = resources[resource]
        if not resource_ele >= menu_ele:
            print(f"Sorry, Insufficient {resource}")
            flag = False
            break
    if flag:
        return 0


def make_coffee(opt):
    for resource, ele in zip(resources, MENU[opt]["ingredients"]):
        resources[resource] -= MENU[opt]['ingredients'][ele]
    print(f"Here is your {opt}, Enjoy!")


def take_money(opt, balance):
    cost = MENU[opt]["cost"]
    print("Please Insert Coins.")
    cash = 0

    for statement in CASH_STATEMENTS:
        cash += int(input(statement)) * CASH_STATEMENTS[statement]

    if cash >= cost:
        balance += cost
        # Calling function to make coffee
        make_coffee(opt)
        change = cash - cost
        if change > 0:
            print(f"Here is ${round(change,2)} in change")
        return balance
    else:
        print("Sorry, Insufficient money!")
        print(f"Here is you cash {cash}")


menu = [ele for ele in MENU]
machine = True
while machine:
    user_option = input("What would you like? (espresso/latte/cappuccino): ").lower()
    if user_option == 'report':
        display_report()
    elif user_option == 'off':
        machine = False
    elif user_option in menu:
        if check_ingredients(user_option) == 0:
            money += take_money(user_option, money)
    else:
        print("Incorrect Option")