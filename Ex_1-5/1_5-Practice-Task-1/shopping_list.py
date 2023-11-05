class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    #adds an item to shopping list
    def add_item(self, item):
        self.shopping_list.append(item)
    #removes an item from shopping list
    def remove_item(self, item):
        self.shopping_list.remove(item)
    #view items in shopping list
    def view_list(self):
        print(self.shopping_list)

#create new object from ShoppingList class
pet_store_list = ShoppingList('Pet_Store_Shopping_List')

#add items to Pet_Store_Shopping_List shopping list
pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collars')
pet_store_list.add_item('flea collars')

#remove items from shopping list
pet_store_list.remove_item('flea collars')

pet_store_list.add_item('frisbee')

pet_store_list.view_list()

