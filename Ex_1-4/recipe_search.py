import pickle

def display_recipe(recipe):
    print(f"Recipe Name: {recipe['name']}\nCooking Time: {recipe['cooking_time']}\nIngredients: {recipe['ingredients']}\nDifficulty: {recipe['difficulty']}")

def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    print("List of all the ingredients used in the recipes")
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}: {ingredient}")
    try:
        #user picks a number from the list
        ingredient_searched = int(input('Pick a number from the list of ingredients: '))
        print('Recipes:')
        for recipe in data['recipes_list']:
            if all_ingredients[ingredient_searched] in recipe['ingredients']:
                display_recipe(recipe)
    except ValueError:
        print("Your input is not a number.")
    except IndexError:
        print('Number not part of list of ingredients')
    except:
        print("The input is incorrect.")
        

#input the name of the file that contains recipe data
filename = input('Enter the file name for the recipes data without the extension name: ') + '.bin'
try:
    my_file = open(filename, 'rb')
    data = pickle.load(my_file)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
except:
    print("An unexpected error occurred.")
else:
    search_ingredient(data)
finally:
    print("Thanks for using the Recipes App")


