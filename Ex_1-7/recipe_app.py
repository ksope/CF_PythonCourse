#import function which will be used to connect to database
from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/task_database")

#import function that generates declarative class
from sqlalchemy.ext.declarative import declarative_base

#generate class from declarative base function for ORM
Base = declarative_base()

#import type which will be used to intializ object Column
from sqlalchemy import Column
#import additional data types which will be used to represent INT & VARCHAR data types
from sqlalchemy.types import Integer, String

#import sessionmake method to create a session on database
from sqlalchemy.orm import sessionmaker

#create session object which will be used to make changes to database and bind to engine
Session = sessionmaker(bind=engine)

#initialize session object
session = Session()

#define Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + self.difficulty + ">"

    def __str__(self):
         return (
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            "-----------------------------\n"
        )

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients.split(', ')) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients.split(', ')) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients.split(', ')) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients.split(', ')) >= 4:
            self.difficulty = 'Hard'

    def return_ingredients_as_list(self):
        results = self.ingredients
        if not results:
            return results
        else:
            return results.split(', ')

#create the Recipes table in the database
Base.metadata.create_all(engine)



def create_recipe(session):
    name_entry = input('Please enter the name of the recipe: ')
    ingredient_entry = input('Enter each ingredient you require seperated by a comma and a space e.g. salt, sugar: ')
    cooking_time_entry = int(input('Please enter the cooking time in minutes: '))
    
    if len(name_entry) > 50 or name_entry.isalnum():
        print('invalid Entry for Recipe name')
    elif len(ingredient_entry) > 255:
        print('Entry for Recipe ingredients exceeds 255 characters')
    

    recipe_entry = Recipe(
        name=name_entry, ingredients=ingredient_entry, cooking_time=cooking_time_entry
    )
    #calculate the dificulty level for the recipe_entry object
    recipe_entry.calculate_difficulty()

    #add recipe_entry to database using the session object
    session.add(recipe_entry)
    session.commit()
    print("Recipe created successfully.")

#retrieve all recipes from the database as a list
def view_all_recipes(session):
    all_recipes = session.query(Recipe).all()
    if not all_recipes:
        return None
    else:
        for recipe in all_recipes:
            print('')
            print(recipe)

#search for recipe by ingredients
def search_by_ingredients(session):
    results = session.query(Recipe.ingredients).distinct().all()
    all_ingredients = set()
    for (ingredient,) in results:
        all_ingredients.update(ingredient.split(", "))

    if not all_ingredients:
        print("There are no ingredients in the database.")
        return
    
    #display list of ingredients to user
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}: {ingredient}")

    try:
        #user picks a number from the list
        recipe_ingredient_numbers = input('Enter the numbers of the ingredients you want to search for, separated by spaces: ').split()
        search_ingredients = [
        list(all_ingredients)[int(index) - 1]
        for index in recipe_ingredient_numbers
        if index.isdigit()
    ]
        
    except ValueError:
        print("One or more of your inputs aren't numbers.")
        return None
    except IndexError:
        print('Number not part of list of ingredients')
    except:
        print("Oops, we've stumbled on some unexpected error.")
        return None
    else:
        conditions = [
        Recipe.ingredients.like(f"%{like_term}%") for like_term in search_ingredients
        ]
        recipes = session.query(Recipe).filter(*conditions).all()

        for recipe in recipes:
            print(recipe)
    session.commit()

#function to update recipe name, cooking time or list of ingredients
def edit_recipe(session):
    recipes = session.query(Recipe).all()
    if len(recipes) > 0:
        results = session.query(Recipe.id, Recipe.name).all()
        for recipe_id, recipe_name in results:
            print(f"{recipe_id}.\t{recipe_name}")
        
        try:
            recipe_id_to_edit = int(input("Select a recipe to update by entering the id number: "))

        except ValueError:
            print("One or more of your inputs aren't numbers.")
        except:
            print("Oops, we've stumbled on some unexpected error.")
        else:
            print("Select an option to update")
            print("Enter 1 to update name\nEnter 2 to update cooking_time\nEnter 3 to update ingredients\n")

        #check whether there is a recipe with an ID of the number inputted
        recipe_to_edit = session.query(Recipe).get(recipe_id_to_edit)
        if not recipe_to_edit:
            print("Recipe not found.")
            return
        else:
            print(recipe_to_edit)
            print('')
            print("Select an option to update")
            print("Enter 1 to update name\nEnter 2 to update cooking_time\nEnter 3 to update ingredients\n")

            #list of possible options
            list_of_choices = ['1','2','3']
            choice_option = input("Your choice: ")
            if not choice_option in list_of_choices:
                print('Please enter a number from the list of options')
                choice_option = input("Your choice: ")
            elif choice_option == '1':
                new_name = input("Enter new name: ")
                if len(new_name) > 50 or new_name.isalnum():
                        print('invalid Entry for Recipe name')
                        return None
                recipe_to_edit.name = new_name
            elif choice_option == '2':        
                try:
                    new_cooking_time = int(input("Enter new cooking_time in mins: "))
                except ValueError:
                    print("Your input is not a number.")
                except:
                    print("Oops, we've stumbled on some unexpected error.")
                else:
                    recipe_to_edit.cooking_time = new_cooking_time
                    recipe_to_edit.calculate_difficulty()
            elif choice_option == '3':
                new_ingredients_entry = input("Enter new ingredients seperated by a comma and a space e.g tea, milk, sugar: ")
                if len(ingredient_entry) > 255:
                    print('Entry for Recipe ingredients exceeds 255 characters')
                    return None
                recipe_to_edit.ingredients = new_ingredients_entry
                recipe_to_edit.calculate_difficulty()
    
    session.commit()
    print("Updated recipe successfully.")
        
#function to delete recipe from table
def delete_recipe(session):
    recipes = session.query(Recipe).all()
    if len(recipes) > 0:
        results = session.query(Recipe.id, Recipe.name).all()
        for recipe_id, recipe_name in results:
            print(f"{recipe_id}.\t{recipe_name}")

        try:
            recipe_id_to_delete = int(input("Select a recipe to update by entering the id number: "))

        except ValueError:
            print("One or more of your inputs aren't numbers.")
        except:
            print("Oops, we've stumbled on some unexpected error.")
        else:
            #check whether there is a recipe with an ID of the number inputted
            recipe_to_delete = session.query(Recipe).get(recipe_id_to_delete)
        if not recipe_to_delete:
            print("Recipe not found.")
            return None
        else:
            print(recipe_to_delete)
        print('')
        delete_option = input(f"Are you sure you want to delete {recipe_to_delete.name} from the database? Enter 'yes' to delete and 'no' to cancel action:  ")

        if delete_option.lower() == 'yes':
            recipe_to_be_deleted = session.query(Recipe).filter(Recipe.id == recipe_id_to_delete).one()
            session.delete(recipe_to_be_deleted)
            session.commit()
            print("Recipe deleted successfully.")


#This is our loop running the main menu
#It continues to loop as long as the user
#doesn't choose to quit

#main menu function
def main_menu(session):
    # Displaying options and handling user input
    choice = ''
    while(choice != quit):
        print("Main Menu")
        print("-"*20)
        print("Pick a choice:")
        print("\t1. Create a new recipe")
        print("\t2. View all recipes")
        print("\t3. Search for a recipe by ingredient")
        print("\t4. Edit an existing recipe")
        print("\t5. Delete a recipe")
        print("\tType 'quit' to exit the program")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_recipe(session)
        elif choice == '2':
            view_all_recipes(session)
        elif choice == '3':
            search_by_ingredients(session)
        elif choice == '4':
            edit_recipe(session)
        elif choice == "5":
            delete_recipe(session) 
        elif choice.lower() == "quit": 
            print("You have chosen to exit the Recipes program")
            break
        else:
            print("Invalid input. Please try again.")


main_menu(session)
# Closing the session and engine when the application is terminated
session.close()
engine.dispose()



