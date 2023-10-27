recipes_list = []
ingredients_list = []


def take_recipe():
    name = input('Please enter the name of the recipe: ')
    cooking_time = int(input('Please enter the cooking time in minutes: '))
    ingredients = input('Enter each ingredient you require seperated by a comma: ').split(', ')
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe


n = int(input('How many recipes will you like to enter: '))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)


for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] > 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'

    print("")
    print(f"Recipe: {recipe['name']} \nCooking Time (min): {recipe['cooking_time']}")
    print('Ingredients:')
    for i in range(len(recipe['ingredients'])):
        print(f"{recipe['ingredients'][i]}")
    print(f"Difficulty level: {recipe['difficulty']}")
    print("------------------------------------------")

print('')
print('Ingredients Available Across All Recipes')
print('----------------------------------------')
for i in ingredients_list:
    print(i)




