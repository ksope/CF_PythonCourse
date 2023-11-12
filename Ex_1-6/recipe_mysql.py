#import the sql connector module
import mysql.connector

#initialize a connection object
conn = mysql.connector.connect(host = 'localhost', user = 'cf-python', passwd = 'password')

#initialize a cursor object from conn
cursor = conn.cursor()

#create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

#connect to the database
cursor.execute("USE task_database")
#create a Table to hold details of a recipe
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
 )''')

def display_recipe(recipe):
    print("\nID:", recipe[0])
    print("Name:", recipe[1])
    print("Ingredients:", recipe[2])
    print("Cooking Time (mins):", recipe[3])
    print("Difficulty:", recipe[4])
    print('')

#update the difficulty of a recipe based on it's ID
def update_difficulty_level(id):
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (id, ))
    results = cursor.fetchall()
    check_ingredients = results[0][2].split(', ')
    check_cooking_time = results[0][3]
    if id == results[0][0]:
        updated_difficulty = calculate_difficulty(check_cooking_time, check_ingredients)
        print("Updated difficulty:", updated_difficulty)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, id))
        new_results = cursor.fetchall()
        for row in new_results:
            display_recipe(row)

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'Easy'
        return difficulty
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'Medium'
        return difficulty
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = 'Intermediate'
        return difficulty
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = 'Hard'
        return difficulty

#Create a new recipe
def create_recipe(conn, cursor):
    name = input('Please enter the name of the recipe: ')
    cooking_time = int(input('Please enter the cooking time in minutes: '))
    ingredient_list = input('Enter each ingredient you require seperated by a comma and a space e.g. salt, sugar: ').split(', ')

    #calculate dificulty leverl
    difficulty = calculate_difficulty(cooking_time, ingredient_list)

    #convert ingredients list to a string
    ingredients = ', '.join(ingredient_list)

    mySql_insert_query = """INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) 
                                VALUES (%s, %s, %s, %s) """
    recipe_entry = (name, ingredients, cooking_time, difficulty)

    cursor.execute(mySql_insert_query, recipe_entry)
    conn.commit()


#Search for a recipe
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    #insert each ingredient to a new list of ingredients and ensure they are not duplicated
    for row in results:
        for ingredients_in_row in row:
            recipe_ingredient_list = ingredients_in_row.split(', ')
            for i in recipe_ingredient_list:
                if not i in all_ingredients:
                    all_ingredients.append(i)
    
    for index, ingredient in enumerate(all_ingredients, start=1):
        print(f"{index}: {ingredient}")

    try:
        #user picks a number from the list
        recipe_ingredient = int(input('Pick a number from the list of ingredients: '))
        all_ingredients_list = list(enumerate(all_ingredients))
        search_ingredient = all_ingredients_list[recipe_ingredient - 1][1]
        print(search_ingredient)
        sql = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
        val = ('%' + search_ingredient + '%', )

        cursor.execute(sql, val)
        recipe_results = cursor.fetchall()

        for row in recipe_results:
            display_recipe(row)
        
    except ValueError:
        print("Your input is not a number.")
    except IndexError:
        print('Number not part of list of ingredients')
    except mysql.connector.Error as error:
        print("Error: {}".format(error))
    except:
        print("The input is incorrect.")
    else:
        conn.commit();
        

#Update an existing recipe
def update_recipe(conn, cursor):
    print("\nAll Recipes:")
    print("-"*20)
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    id_list = []
    #Get all the recipes
    if len(results) == 0:
        print("\nThere are no recipes currently available")
    else:
        for row in results:
            display_recipe(row)
            id_list.append(row[0])

    #user selects column that needs an update
    try:
        recipe_id = int(input("Select a recipe to update by entering the id number: "))
    except:
        if not recipe_id in id_list:
            print("Number entered is not an ID of any recipe")
    else:
        print("Select an option to update")
        print("Enter 1 to update name\nEnter 2 to update cooking_time\nEnter 3 to update ingredients\n")
    
    #list of possible options
    list_of_choices = ['1','2','3']
    choice_option = input("Your choice: ")
    if not choice_option in list_of_choices:
        print('Please enter a number from the list of options')
        choice_option = input("Your choice: ")
    elif choice_option == '1':
        new_value = input("Enter new name: ")
        sql = "UPDATE Recipes SET name = %s WHERE id = %s"
        val = (new_value, recipe_id)
        cursor.execute(sql, val)
    elif choice_option == '2':
        new_value = input("Enter new cooking_time in mins: ")
        sql = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        val = (new_value, recipe_id)
        cursor.execute(sql, val)
        update_difficulty_level(recipe_id)
    elif choice_option == '3':
        new_value = input("Enter new ingredients seperated by a comma and a space e.g tea, milk, sugar: ")
        sql = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        val = (new_value, recipe_id)
        cursor.execute(sql, val)
        update_difficulty_level(recipe_id)
    
    print("Updated recipe successfully.")
    conn.commit()


#Delete a recipe
def delete_recipe(conn, cursor):
    #display full list of recipes
    print("\nAll Recipes:")
    print("-"*20)
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    id_list = []
    #Get all the recipes
    if len(results) == 0:
        print("\nThere are no recipes currently available")
    else:
        for row in results:
            display_recipe(row)
    
    id_to_delete = int((input("\nEnter the ID of the recipe you want to delete: ")))
    # Delete the recipe
    cursor.execute("DELETE FROM Recipes WHERE id = (%s)", (id_to_delete, ))

    # Commit changes
    conn.commit()
    print("\nRecipe was deleted successfully.")



#This is our loop running the main menu
#It continues to loop as long as the user
#doesn't choose to quit

#main menu function
def main_menu(conn, cursor):
    choice = ''
    while(choice != quit):
        print("Main Menu")
        print("-"*20)
        print("Pick a choice:")
        print("\t1. Create a new recipe")
        print("\t2. Search for a recipe by ingredient")
        print("\t3. Update an existing recipe")
        print("\t4. Delete a recipe")
        print("\tType 'quit' to exit the program")
        choice = input("Your choice: ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        else:
            print("You have chosen to exit the Recipes program")
            break


main_menu(conn, cursor)

if conn.is_connected():
        cursor.close()
        conn.close()
        print("Recipes program closed")

    

