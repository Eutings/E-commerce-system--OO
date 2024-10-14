

import json


# ---------------2.1 Defining the domain classes (10 points)-------------------
class Product:

    def __init__(self,name,price,quantity,brand,ui):
        #Attributes
        self.name = str(name)
        self.price = float(price)
        self.quantity = int(quantity)
        self.brand = str(brand)
        self.ui = ui       #ui is unique identifier, which will be clarify in class ShoppingCart. Not here


    def to_json(self):
        # returns the JSON-formatted representation of the product.
        return json.dumps({
            'name':self.name,
            'price':self.price,
            'quantity':self.quantity,
            'unique_identifier':self.ui,
            'brand':self.brand
        })

# -***************Subclass***
class Clothing(Product):

    def __init__(self,name,price,quantity,brand,ui,size,material):
        super().__init__(name,price,quantity,brand,ui)
        self.size = size
        self.material = material


    def to_json(self):
        return json.dumps({
            'name':self.name,
            'price':self.price,
            'quantity':self.quantity,
            'unique_identifier':self.ui,
            'brand':self.brand,
            'size':self.size,
            'material':self.material
        })

class Food(Product):

    def __init__(self,name,price,quantity,brand,ui,expiry_date,gluten_free,suitable_for_vegans):
        super().__init__(name,price,quantity,brand,ui)
        self.expiry_date = expiry_date
        self.gluten_free = gluten_free
        self.suitable_for_vegans = suitable_for_vegans

    def to_json(self):
        return json.dumps({
            'name':self.name,
            'price':self.price,
            'quantity':self.quantity,
            'unique_identifier':self.ui,
            'brand':self.brand,
            'expiry_date':self.expiry_date,
            'gluten_free': self.gluten_free,
            'suitable_for_vegans': self.suitable_for_vegans
        })

class Cup(Product):

    def __init__(self, name, price, quantity, brand,ui, color, material):
        super().__init__(name, price, quantity, brand, ui)
        self.color = color
        self.material = material

    def to_json(self):
        return json.dumps({
            'name':self.name,
            'price':self.price,
            'quantity':self.quantity,
            'unique_identifier':self.ui,
            'brand':self.brand,
            'color':self.color,
            'material':self.material
        })

#------------Product class and Subclass end ----------------

# -------------------ShoppingCart class-------------------
class ShoppingCart():

    _cart = {}

    def __init__(self):
        pass

    def get_cart(self):
        return self._cart

    def price_input(self):
        #input price to be float
        while True:
            price = input("Insert its price (£): ")
            if price.isdigit() is True:
                return float(price)
            else:
                print("invalid value! enter again")
                return self.price_input()

    def quantity_input(self):
        # input quantity to be int
        while True:
            quantity = input("Insert its quantity:")
            if quantity.isdigit() is True and int(quantity)>=1:
                if float(quantity).is_integer():
                    return int(quantity)
                else:
                    print("invalid value! enter again")
            else:
                print("invalid value! enter again")
                return self.quantity_input()

    def ui_input(self):
        #input unique identifier to be a 13 digit sequence and unique
        while True:
            ui = str(input("Insert its EAN code:"))
            if len(ui)!=13 or not ui.isdigit():
                print("EAN code should be a 13 digit sequence! Enter again!")
                return self.ui_input()
            elif ui in self._cart.keys():
                print("EAN code exist,it should be unique! Enter again!")
                return self.ui_input()
            else:
                return ui

    def expiry_date_input(self):
        #input expiry date as data type
        while True:
            expiry_date = input("Insert its expiry_date(dd/mm/YYYY):")
            try:
                day, month, year = map(int, expiry_date.split('/'))
                if year<1111 or year>9999 or month<1 or month >12 or day<1 or day >31:
                    print("Invalid value!")
                    return self.expiry_date_input()
                elif month in [4,6,9,11] and day >30:
                    print("Invalid value!")
                    return self.expiry_date_input()
                elif month ==2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) and day>29:
                    print("Invalid value!")
                    return self.expiry_date_input()
                elif month ==2 and day>28:
                    print("Invalid value!")
                    return self.expiry_date_input()
                else:
                    return expiry_date
            except:
                return self.expiry_date_input()

    def gluten_free_input(self):
        # set Yes or No for "gluten_free"
        gluten_free = str(input("Insert its gluten_free(Y or N):"))
        if gluten_free in ("Y","N"):
            return gluten_free
        else:
            print("Invalid value!")
            return self.gluten_free_input()

    def suitable_for_vegans_input(self):
        # set Yes or No for "suitable_for_vegans"
        suitable_for_vegans = str(input("Insert its suitable_for_vegans(Y or N):"))
        if suitable_for_vegans in ("Y", "N"):
            return suitable_for_vegans
        else:
            print("Invalid value!")
            return self.suitable_for_vegans_input()



    def input_product(self):
        try:
            type = input("Insert its type: ")
            name = input("Insert its name: ")
            price = self.price_input()
            quantity = self.quantity_input()
            brand = input("Insert its brand:")
            ui = self.ui_input()
            if type == "Clothing" or type == "clothing":
                size = input("Insert its size:")
                material = input("Insert its material:")
                p = Clothing(name, price, quantity, brand, ui, size, material)
                return p
            elif type == "Food" or type == "food":
                expiry_date = self.expiry_date_input()
                gluten_free = self.gluten_free_input()
                suitable_for_vegans = self.suitable_for_vegans_input()
                p = Food(name, price, quantity, brand, ui, expiry_date, gluten_free, suitable_for_vegans)
                return p
            elif type == "Cup" or type == "cup":
                color = input("Insert its color:")
                material = input("Insert its material:")
                p = Cup(name, price, quantity, brand, ui, color, material)
                return p
            else:
                p = Product(name, price, quantity, brand, ui)
                return p
        except:
            return self.input_product()

    #*********************The shopping system (10 points)********
    def addProduct(self):
        #add a new product
        print("Adding a new product:")
        p = ShoppingCart().input_product()
        add_product = json.loads(p.to_json())
        self._cart[add_product['unique_identifier']] = add_product
        print("The product {} has been added to the cart.".format(p.name))
        print("The cart contains {} products.".format(len(self._cart)))

    def removeProduct(self):
        # remove product by unique identifier
        print("Removing a product:")
        del_ui = input("Insert its EAN code:")
        if del_ui not in self._cart.keys():          #the product should exist in cart!
            print("product not exist")
            print("Please type 'E' to output a file and check the exist product")
        else:
            self._cart.pop(del_ui,None)

            print("The product with {} EAN code has been remove from the cart.".format(del_ui))
        print("The cart contains {} products.".format(len(self._cart)))

    def getContents(self):
        return sorted(self._cart.items(), key = lambda x: x[1]["name"])

    def changeProductQuantity(self, p, q):
        # p is product, q is quantity. product should be exist and quantity should be positive int.
        if str(p) in self._cart:
            if p.isdigit() and int(p)>=1:
                if float(p).is_integer():
                    self._cart[p]['quantity'] = int(q)
                    print("{}'s quantity change to {} already".format(p,q))
                else:
                    print("quantity should be positive int")
            else:
                print("quantity should be positive int")
        else:
            print("Product not exist in cart, nothing change!")    #let the user specify a product without ambiguity
                                                                    # and, if no product is found, no changes should take place





#------------------------Shopping actions -------------------------------------------------------

user_cart = ShoppingCart()
print('The program has started.')
print('Insert your next command (H for help):')
terminated = False
while not terminated:
    c = input("Type your next command:")
    if c in ('T','t'):
        terminated = True
    elif c in ('A','a'):
        user_cart.addProduct()
    elif c in ('R','r'):
        user_cart.removeProduct()
    elif c in ('S','s'):
        ls = user_cart.getContents()
        print("This is the total of the expenses:")
        total_price =0
        for i in range(len(ls)):
            quantity =ls[i][1]['quantity']
            name = ls[i][1]['name']
            price = ls[i][1]['price']
            total_price += quantity*price
            if quantity == 1:
                q = ''
            else:
                q = ' {} *'.format(quantity)
            print("{} -{} {} = £{}".format(i+1,q,name,quantity*price))
        print('Total = £{}'.format(total_price))
    elif c in ('Q','q'):
        print("Change quantity by using EAN code.")
        p = str(input("Insert its EAN code:"))
        q = user_cart.quantity_input()
        user_cart.changeProductQuantity(p, q)

    elif c in ('E','e'):
        # export
        f = input("Enter the file name (.json)Exported:")
        if f[-5:] == '.json':
            json_data = json.dumps(user_cart.get_cart(), indent=3)
            with open(f, 'w') as file:
                file.write(json_data)
                print("File 'Exported' correctly saved.")

    elif c in ('H','h'):
        print("The program supports the following commands:\
        \n[A] - Add a new product to the cart\
        \n[R] - Remove a product from the cart\
        \n[S] - Print a summary of the cart\
        \n[Q] - Change the quantity of a product\
        \n[E] - Export a JSON version of the cart\
        \n[T] - Terminate the program\
        \n[H] - List the supported commands")

    else:
        print("Command not recognised. Please try again")

print( 'Goodbye.' )
# -----------------------Shopping actions end--------------------------------



