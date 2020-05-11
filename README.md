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
