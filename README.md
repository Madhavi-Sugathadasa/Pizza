# Pizza

Created a web application for handling a pizza restaurant’s online orders using **Django** Framework &amp; **Stripe payment**.

---

### Features

Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

1. **Menu**: The web application will support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge). 

2. **Adding Items**: Using Django Admin, site administrators (restaurant owners) will be able to add, update, and remove items on the menu. 

3. **Registration, Login, Logout**: Site users (customers) will be able to register for the web application with a username, password, first name, last name, and email address. Customers will then be able to log in and log out of the website.

4. **Shopping Cart**: Once logged in, users will see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping will be saved even if a user closes the window, or logs out and logs back in again.

5. **Placing an Order**: Once there is at least one item in a user’s shopping cart, they will be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total before placing an order.

6. **Viewing Orders**: Site administrators will have access to a page where they can view any orders that have already been placed.

Apart from the features mentioned in the project specification, for the **personal touch**, I added **two features**, integrated with the **Stripe API**. It would allow the actual users to use their credit cards in order to make a purchase during checkout and also allow site administrators to **mark orders as complete** and allow users to see the **status of their pending or completed orders**


---

Below is a brief description about the project structure.

---

**Menu**

In order to represent  all available menu items, 4 tables were created.

1. **_Menu_Types table - (Menu_Type model)_**
 used to display  main categories such as Regular Pizza, Sicilian Pizza, subs etc.
 
_name_ field is used for category name and _display_order_  field for displaying hierarchy  of the categories on the  website. For example if you have decided to display Subs category before Regular Pizza  category, you just need to assign a integer value to Subs higher than Regular pizza

2. **_Menu_Items table - (Menu_Item model)_**
used to display each menu item in the menu

_type_id_ field to decide under which Menu_Type category each item falls

_Item_name_ field for the name of the menu item

_Image_ field for uploading an Image for each menu item - recommended Image size 350 px by 235px 

_No_of_toppings_ field for keeping required no. of toppings for each item, default value is 0 and i.e. no topping selection required for that item

_is_mult_cat_ field is a boolean field. If item has multiple size categories such as Small or Large, this value is set to True or otherwise set to False

_small_price_ field for small size item price

_large_price_ field for large size item price

**_Note_:** if item hasn’t got multi size categories such as small or large, you need to set is_mult_cat to False and then add price either to small_price field or large_price field


3. **_Toppings table (Topping model)_**
used to keep details of all available toppings for pizzas

_name_ field for name of the topping

4. **_Additions table (Addition model)_**
used to keep details of all available additions (add-ons) for subs 

_name_ field for name of the addition

_small_price_ field for keep price of adding this addition to a small size sub 

_large_price_ field for keep price of adding this addition to a large size sub

---