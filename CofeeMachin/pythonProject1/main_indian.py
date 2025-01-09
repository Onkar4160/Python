MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 150,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 250,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 300,
    }
}

profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}
def is_resources_sufficient (order_ingredients):
    '''Returns the plentyness of ingredients.'''
    for item in order_ingredients:
        if order_ingredients[item] >= resources[item]:
            print (f"Sorry there is not enough {item}")
            return False
    return True

def process_coins():
    '''Returns the totel calculated from the coin inserted'''
    print ("Please enter the notes.")
    totel = int (input("how many 500's notes?: "))* 500
    totel += int(input("how many 200's notes?: ")) * 200
    totel += int(input("how many 100's notes?: ")) * 100
    totel += int(input ("how many 50's notes?: ")) * 50
    totel += int(input ("how many 20's notes?: ")) * 20
    totel += int(input ("how many 10's notes?: ")) * 10
    return totel

def is_transection_successfull (money_recived , drink_cost) :
    '''returns True if the payment is accepted.'''
    if money_recived >= drink_cost:
        change = round (money_recived - drink_cost, 2)
        print (f"here is  ₹{change} in change")
        global profit
        profit += drink_cost
        return True
    else :
        print ("Sorry that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name , order_ingredients):
    '''deduct the used ingredients from the resources.'''
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print (f"here is your {drink_name} ☕, Enjoy !")


is_on = True
while is_on:
    choice = input ("What would you like to take? (espresso/latte/cappuccino): ")
    if choice =="off":
        is_on = False
    elif choice =="report":
        print (f"Water: {resources["water"]}ml")
        print (f"Milk: {resources["milk"]}ml")
        print (f"Coffee: {resources["coffee"]}g")
        print (f"Money: ${profit}")
    else :
        drink = MENU[choice]
        if is_resources_sufficient(drink["ingredients"]):
            payment = process_coins()
            if is_transection_successfull(payment, drink["cost"]):
                make_coffee(choice, drink["ingredients"])