import random, os

os.system('cls')
print("\nSANDWICH MAKER 9000")

breads = ["White Bread", "Kaiser Roll", "Sub Roll", "Ciabatta", "Wheat Bread"]
cheeses = ["Swiss", "Provolone", "Mozzarella", "American", "Cheddar", "Pepper Jack"]
Protein = ["Roast Beef", "Ham", "Turkey", "Salami", "Chicken Salad", "Tuna Salad", "Pork Bacon", "Grilled Chicken with Italian Seasoning"]
Toasted = [True, False]
Toppings = ["Lettuce", "Arugula", "Red Onion", "Bell Peppers", "Pickles", "Jalapenos"]
Side = "Chips"
Beverage = "Canned Soda"
Condiments = ["Mayo", "Deli Mustard", "Garlic Aioli", "Basil Mayo", "Chipotle Mayo", "Caesar Dressing", "Oil & Vinegar", "Italian", "Oregano"]

numToppings = random.randint(1, 3)
numCondomiments = random.randint(2, 4)

Bread = random.choice(breads)
print(f"\nBread: {Bread}")
Cheese = random.choice(cheeses)
print(f"Cheese: {Cheese}")
Protein = random.choice(Protein)
print(f"Protein: {Protein}")
Toasted = random.choice(Toasted)
print(f"Toasted: {Toasted}")

top = []
sauces = []
for t in range(numToppings):
    top.append(random.choice(Toppings))
for c in range(numCondomiments):
    sauces.append(random.choice(Condiments))

print("Toppings: " + str(top)[1:-1].replace("\'", ""))
print("Condiments: " + str(sauces)[1:-1].replace("\'", ""))
print(f"Side: {Side}")
print(f"Beverage: {Beverage}\n\n")