class Recipe():
    all_ingredients = []
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = ''

    #calculate difficulty level
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Hard'

    #set the name of the recipe
    def set_name(self, name):
        self.name = name
    #get the name of the recipe
    def get_name(self):
        return self.name

    #set the cooking time for each recipe in minutes
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
    #get the cooking time for each recipe in minutes
    def get_cooking_time(self):
        return self.cooking_time

    #add ingredients to a recipe
    def add_ingredients(self, *args):
        self.ingredients = args
        self.update_all_ingredients()

    #print the list of ingredients
    def get_all_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty


    #search for an ingredient in the recipe
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        return False

    #update all ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            self.all_ingredients.append(ingredient)

    def __str__(self):
        output = "\nRecipe Name: " + self.name + \
            "\nCooking Time: " + str(self.cooking_time) + " minutes" + \
                "\nDifficulty: " + self.get_difficulty() + \
                "\nIngredients: \n" 
        for ingredient in self.ingredients:
            output += ingredient + "\n"
        return output

#search for a recipe from a list of recipes
def recipe_search(data, search_term):
    print(f"Recipes that contain {search_term}")
    for recipe in data:
        if recipe.search_ingredient(search_term):
             print(recipe)


recipes_list = []

tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)
print(tea)

recipes_list.append(tea)

coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)
print(coffee)

recipes_list.append(coffee)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)
print(cake)

recipes_list.append(cake)

bananaSmoothie = Recipe('Banana Smoothie')
bananaSmoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
bananaSmoothie.set_cooking_time(5)
print(bananaSmoothie)

recipes_list.append(bananaSmoothie)

# Display string representation of each recipe
#print('')
#print('Recipes List')
#print('----------------------------------------')
#for recipe in recipes_list:
#    print(recipe)

# Search for recipes that contain certain ingredients
print('')
print('Recipes that contain ingredients')
print('----------------------------------------')
for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)






    

    