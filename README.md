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

**Adding items**

All the items were added to DB using the Admin UI 

---

**Registration, Login, Logout**

Following views were created using in Django’s built-in users and authentication system:

_register_view_ for registration

_login_view_ for login

_logout_view_ for logout


---

**Shopping Cart**

Once logged in, users will be taken to the _index_ view and will be able to see the **representation of the restaurant’s menu** with the option to **select each item** of the menu. Once selected a menu item, then user will be taken to _item_ view where they can **add** that item (along with toppings or extras and quantity, if appropriate) to their virtual “**shopping cart**.” 
When users add an item to the cart, they will be taken to the shopping cart page (i.e. _shopping_cart_ view). Also there is a cart icon on top of the Navigation menu and when users click on that icon they will be taken to the shopping cart page.
Once on the shopping cart page, users can **remove items** (_remove_item_ view) in the event the users change their mind.  or  else they can go back to menu and **add more items**. On finalising to place the order, then they need  to **agreed Terms and conditions** of the website and click place order link 

**Note**: when users add items to the shopping card, the latest basket will be saved to the database Carts table (i.e. Cart Model)

So the contents of the shopping will be saved even if a user closes the window or logs out and logs back in again.

**Note**: let’s say if user added items to the shopping cart and logged out, then after 30 days (it can be any number of days), user logs in back and in case some of the items are no longer available, those items will be automatically removed from the basket on the login.

---

**Placing an Order**

Once there is **at least one item** in a user’s shopping cart, they will be able to place an order, whereby the user is asked to confirm the items in the shopping cart and the total, before placing an order. This functionality is handled by the _order_ view.

---

**Payment**

Once users click on the place order link, then they will be redirected to **Stripe’s payment** page.
In order for this functionality to work, there are two environment variables you need to set up before server start up.
_STRIPE_PUBLISHABLE_API_KEY_ and _STRIPE_SECRET_API_KEY_

When you setup a stripe account online there will be a section named “Get your test API keys”, you need to setup _STRIPE_PUBLISHABLE_API_KEY_ with publishable key and _STRIPE_SECRET_API_KEY_ with secret key

Eg:
export STRIPE_PUBLISHABLE_API_KEY = pk_test_Abc

export STRIPE_SECRET_API_KEY = sk_test_dcde


Upon successful payment users will be redirected to _payment_success_ view where **a new order will be created** and **saved** to Database. If user clicks _back_ link on Stripe payment page, then user will be taken to _payment_cancel_ view which will take back to shopping cart page.

As per the stripe documentation, I am creating Stripe Product item for each of our products (if that product is already in Stripes product list, then it will be  retrieved  without creating one) , I decided not to create Stripe prices upfront, so I am creating ad-hoc prices at Checkout Session creation.

**Note** - When your customer completes a payment, Stripe redirects them to the URL that we specified in the success_url parameter. There are several ways you can confirm that the payment is successful, you can use Stripe dashboard for manually process. I decided to use a webhook , but I cannot create a webhook using localhost. So I didn’t implement that part, only when stripe redirect to my payment_success view , I am saving the order & showing user a order confirmation.

---

**Saving orders**

There are **two tables** to handle successful orders.
1. **_Orders table (Order model)_**
_user_ field for keeping customer details of the customer who placed the order

_total_ field for order total

_date_time_ field for keeping date and time of the order

_status_ field - this is a boolean field. If it is True that means order is completed, otherwise order is pending

_payment_ field - this is also a boolean field , if it is true means payment was successful

_payment_session_ field for keeping the payment session id returned by Stripe payment gateway

2. **_Order_Items table (Order_Item model)_**
_order_id_ field for keeping relevant order id from above Orders table

_item_name_ field for item name which is created using menu type and menu item name

_size_ field - if item size was selected it will be saved to this field, otherwise null or blank

_description_ field for keeping selected topping details or addition details if required

_quantity_ field  for number of item

_price_ field total price for this item

---

**Viewing Orders**

There is a different login view for staff login (named _staff_login_view_) and once logged in staff/Site administrators have access to a page where they can **view any orders** that have already been placed. This page allows site administrators/staff to **mark orders as complete**.

On customer’s home page also there is a link to see all orders made by the customer. If staff or site administrators  mark the order as completed, customer will be able to see the status on orders page by clicking on the order.

**Note** - I added pagination for both staff members orders page and customers orders page

---