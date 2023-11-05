import pickle

recipes_list = []
ingredients_list = []

#Take recipes and calculate difficulty 
def take_recipe():
    name = input('Please enter the name of the recipe: ')
    cooking_time = int(input('Please enter the cooking time in minutes: '))
    ingredients = input('Enter each ingredient you require seperated by a comma and a space e.g. salt, sugar: ').split(', ')
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    calc_difficulty(recipe)
    return recipe

def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'

#User enters a filename which will be a binary file            
filename = input('Please enter the name of the file: ') + '.bin'

#open the binary file using a try-except-else-finally block
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
    data = {'recipes_list': recipes_list, 'all_ingredients' : ingredients_list }
except:
    print("An unexpected error occurred.")
    data = {'recipes_list': recipes_list, 'all_ingredients' : ingredients_list }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    ingredients_list = data['all_ingredients']


num_of_recipes = int(input('How many recipes will you like to enter: '))

for i in range(num_of_recipes):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)


#first print all recipes
print('This is the updated recipes and ingredients')
print('')
print('Recipes List')
print('----------------------------------------')
for recipe in recipes_list:
    print(recipe['name'])

#then print all ingredients used
print('')
print('Ingredients Available Across All Recipes')
print('----------------------------------------')
for j in ingredients_list:
    print(j)

#save the data into a file
my_file = open(filename, 'wb')
pickle.dump(data, my_file)
my_file.close()
print(f'Saved data to {filename}')