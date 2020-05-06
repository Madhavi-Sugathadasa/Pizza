from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from .models import Menu_Item, Menu_Type, Topping, Addition, Cart, Order, Order_Item
import json
from datetime import datetime
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
import stripe
from django.conf import settings


stripe.api_key = getattr(settings, "STRIPE_SECRET_API_KEY", None)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username:
            return render(request, "users/customers/login.html", {"message": "Must provide username."})
        if not password:
            return render(request, "users/customers/login.html", {"message": "Must provide password."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # udpate basket with prviously added any items for this user
            # also this will remove any unavailble items in previously saved basket
            saved_basket = Cart.objects.filter(user_id = request.user.id)
            if saved_basket:
                basket = json.loads(saved_basket[0].basket)
                #update basket remove any items unavailable
                for basket_item in list(basket):
                    item = None
                    try:
                        item = Menu_Item.objects.get(pk=basket_item["item"])
                    except Menu_Item.DoesNotExist:
                        pass
                    #if item no longer available
                    if not item:
                        basket.remove(basket_item)
                    else:
                        # if topping is removed from database then remove that item all together
                        toppings = basket_item.get("toppings")
                        if toppings:
                            if item.no_of_toppings != len(toppings):
                                basket.remove(basket_item)
                            else:
                                for topping_item in toppings:
                                    topping = None
                                    try:
                                        topping = Topping.objects.get(pk=topping_item["id"])
                                    except Topping.DoesNotExist:
                                        pass
                                    if not topping:
                                        basket.remove(basket_item)
                                        break
                        else:
                            if item.no_of_toppings > 0:
                                basket.remove(basket_item)
                        
                        # if selected extra is removed from database then remove that item all together
                        extras = basket_item.get("extras") 
                        if extras:
                            for add_on_item in extras:
                                add_on = None
                                try:
                                    add_on = Addition.objects.get(pk=add_on_item["id"])
                                except Addition.DoesNotExist:
                                    pass
                                if not add_on:
                                    basket.remove(basket_item)
                                    break
                
                # Save filtered basket back to DB
                shopping_cart = Cart()
                shopping_cart.id = saved_basket[0].id
                shopping_cart.date_time = datetime.now()
                shopping_cart.user_id = request.user
                shopping_cart.basket = json.dumps(basket)
                shopping_cart.save()
                request.session['basket'] = basket
                
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/customers/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/customers/login.html", {"message": None})

    
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        if not username:
            return render(request, "users/customers/register.html", {"message": "Must provide username."})
        if not password:
            return render(request, "users/customers/register.html", {"message": "Must provide password."})
        if password != confirm_password:
            return render(request, "users/customers/register.html", {"message": "Passwords didn't match."})
        if not first_name:
            first_name = None
        if not last_name:
            last_name = None
        if not email:
            email = None

        try:
            User.objects.create_user(username=username, password=password,  first_name=first_name, last_name=last_name, email=email)
        except IntegrityError:
            return render(request, "users/customers/register.html", {"message": "User already exists."})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/customers/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/customers/register.html", {"message":None})
    
    
def logout_view(request):
    is_staff = request.user.is_staff
    logout(request)
    #if staff memeber , send to staff login page
    if is_staff:
        return HttpResponseRedirect(reverse("staff_login"))
    else:
        return render(request, "users/customers/login.html", {"message": None})
    

@login_required(login_url='login')
def index(request):
    try:
        dict_menu_items ={}
        # load all menu types on their display order
        menu_types = Menu_Type.objects.all().order_by('display_order')
        for menu_type in menu_types:
            # laod menu items for each menu type
            selected_items = Menu_Item.objects.filter(type_id = menu_type.id)
            if selected_items:
                dict_menu_items[menu_type.id] = selected_items
    except Menu_Type.DoesNotExist:
        return render(request, "error.html", {"message": "Menu types does not exist."})
    except Menu_Item.DoesNotExist:
        return render(request, "error.html", {"message": "Menu items does not exist."})
    
    context = {"menu_types":menu_types, "menu_items":dict_menu_items, "user":request.user}
    return render(request, "index.html", context)


@login_required(login_url='login')
def item(request, menu_id):
    # load selected menu item details
    try:
        item = Menu_Item.objects.get(pk=menu_id)
    except Menu_Item.DoesNotExist:
        return render(request, "error.html", {"message": "item does not exist."})
    context = {
      "item": item
    }
    if item.no_of_toppings > 0:
        toppings = Topping.objects.all()
        context["toppings"] = toppings
    if item.type_id.name == 'Subs':
        additions = Addition.objects.all()
        context["additions"] = additions
    
    return render(request, "order/item.html", context)


@login_required(login_url='login')
def add(request, menu_id):
    # add selected menu item to the basket
    try:
        item = Menu_Item.objects.get(pk=menu_id)
    except KeyError:
        return render(request, "error.html", {"message": "No selection."})
    except Menu_Item.DoesNotExist:
        return render(request, "error.html", {"message": "No menu item."})
    
    dict_item_selection = {}
    size = None
    toppings = []
    extras = []
    quantity = 0
    
    # read quantitiy
    try:
        quantity = int(request.POST["quantity"])
    except KeyError:
        return render(request, "error.html", {"message": "Invalid quantity."})
    if quantity <= 0:
        return render(request, "error.html", {"message": "Invalid quantity."})
    
    # if item has mutiple sizes, read selected size
    if item.is_mult_cat :
        size = request.POST["size"]
        if not size :
            return render(request, "error.html", {"message": "Please choose the size."})
        if not size in ["S","L"] :
            return render(request, "error.html", {"message": "Invalid size."})
    
    # if item has toppings attached to it, read selected toppings   
    if item.no_of_toppings > 0:
        for i in range(1, item.no_of_toppings + 1):
            try:
                topping_id = int(request.POST["topping_" + str(i)])
                topping = Topping.objects.get(pk=topping_id)
            except KeyError:
                return render(request, "error.html", {"message": "Invalid selection."})
            except Topping.DoesNotExist:
                return render(request, "error.html", {"message": ("Please select topping" + str(i))})
            toppings.append({"id":topping.id, "name":topping.name})
    
    # if item type is 'Subs', read selected add-ons (extras)
    if item.type_id.name == 'Subs':
        additions = Addition.objects.all()
        for addition in additions:
            if request.POST.get("check_" + str(addition.id)):
                try:
                    addition_id = int(request.POST.get("check_" + str(addition.id)))
                    add_on = Addition.objects.get(pk=addition_id)
                except KeyError:
                    return render(request, "error.html", {"message": "Invalid selection."})
                except Addition.DoesNotExist:
                    return render(request, "error.html", {"message": "Invalid selection."})
                extras.append({"id":add_on.id, "name":add_on.name})
    
    
    dict_item_selection["item"] = item.id
    dict_item_selection["item_name"] = item.type_id.name + " - " + item.item_name
   
    if size:
        dict_item_selection["size"] = size
    if toppings:
        dict_item_selection["toppings"] = toppings
    if extras:
        dict_item_selection["extras"] = extras
    
    
    basket = []
    if 'basket' in request.session:
        basket = request.session['basket']
    if not basket:
        basket =[]
    match_found = False
    # if same type of basket item is found on previous items, just increase the quantity of that item, otherwise add item to the basket
    for idx, basket_item in enumerate(basket):
        # Temperary setting quantities to equal to find a exact match, later correct value will be reassign
        dict_item_selection["quantity"] = basket_item["quantity"]
        
        # check item already exists
        if (dict_item_selection == basket_item):
            match_found = True
            basket[idx]["quantity"] += quantity
            break
    # if no match found, update the correct quantity and add to basket & update session
    if not match_found:
        dict_item_selection["quantity"] = quantity
        basket.append(dict_item_selection)
    request.session['basket'] = basket    
    
    # saving basket to the Cart table as a json text, if user log out & login again then previously added basket will display from this saved data
    shopping_cart = Cart()
    saved_basket = Cart.objects.filter(user_id = request.user.id)
    if saved_basket:
        shopping_cart.id = saved_basket[0].id
    shopping_cart.date_time = datetime.now()
    shopping_cart.user_id = request.user
    shopping_cart.basket = json.dumps(basket)
    shopping_cart.save()
    
    return HttpResponseRedirect(reverse("cart"))


@login_required(login_url='login')
def shopping_cart(request):
    # view shopping cart
    basket = []
    if 'basket' in request.session:
        basket = request.session['basket']
        
    # update basket with latest prices and check items are still availble
    basket_total = 0.00
    if basket:
        for idx, basket_item in enumerate(basket):
            item_total_price = 0.00
            item = None
            try:
                item = Menu_Item.objects.get(pk=basket_item.get("item"))
            except Menu_Item.DoesNotExist:
                    return render(request, "error.html", {"message": "Some of the basket items are no longer availble."})
            if item:
                size = basket_item.get("size")
                if not size:
                    item_total_price += item.small_price if item.small_price else item.large_price
                else:
                    if size == 'S':
                        item_total_price += item.small_price 
                    elif size == 'L':
                        item_total_price += item.large_price
                
                toppings = basket_item.get("toppings")
                if toppings:
                    for topping in toppings:
                        topping_item = None
                        try:
                            topping_item = Topping.objects.get(pk=topping["id"])
                        except Topping.DoesNotExist:
                            return render(request, "error.html", {"message": "Some toppings are no longer availble."})
                
                extras = basket_item.get("extras")
                
                if extras:
                    for add_on in extras:
                        add_on_item = None
                        try:
                            add_on_item = Addition.objects.get(pk=add_on["id"])
                        except Addition.DoesNotExist:
                            return render(request, "error.html", {"message": "Some add ons are no longer availble."})
                        if add_on_item:
                            if size:
                                if size == 'S':
                                    item_total_price += add_on_item.small_price
                                elif size == 'L':
                                    item_total_price += add_on_item.large_price
                quantity = basket_item.get("quantity")
                item_total_price *= quantity
                basket[idx]["price"] = item_total_price
                basket_total += item_total_price
            else:
                return render(request, "error.html", {"message": "Invalid cart item."})
    
    # setting session variables order total and order_items
    request.session['order_total'] = basket_total
    request.session['order_items'] = basket
    
    context = {
        "basket": basket,
        "basket_total":basket_total
    }
    return render(request, "order/basket.html", context)


@login_required(login_url='login')
def remove_item(request, cart_id):
    # remove selected item form the basket
    basket = []
    
    if 'basket' in request.session:
        basket = request.session['basket']
        
    basket_length = len(basket)
    if basket_length < cart_id:
        return render(request, "error.html", {"message": "Invalid cart item."})
    basket.pop(cart_id - 1)
    request.session['basket'] = basket
    
    shopping_cart = Cart()
    saved_basket = Cart.objects.filter(user_id = request.user.id)
    if saved_basket:
        shopping_cart.id = saved_basket[0].id
    if basket:
        shopping_cart.date_time = datetime.now()
        shopping_cart.user_id = request.user
        shopping_cart.basket = json.dumps(basket)
        shopping_cart.save()
    else:
        # if basket is empty remove cart from DB
        shopping_cart.delete()
    return HttpResponseRedirect(reverse("cart"))


@login_required(login_url='login')
def order(request):
    # redirect customer to stripe payment page
    
    # check whether user agreed to terms and conditions
    try:
        terms_agreement = request.POST["terms_agreement"]
    except KeyError:
        return HttpResponseRedirect(reverse("cart"))
    
    order_items = []
    if 'order_items' in request.session:
        order_items = request.session['order_items']
    else:
        return render(request, "error.html", {"message": "Invalid request."})
    if not order_items:
        return render(request, "error.html", {"message": "There are no items in the cart."})
    order_total = 0.00
    if 'order_total' in request.session:
        order_total = float(request.session['order_total'])
    else:
        return render(request, "error.html", {"message": "Invalid request."})
    
    stripe_price_items = []
    
    for order_item in order_items:
        item_name = order_item.get("item_name")
        size = order_item.get("size")
        item_total_price = float(order_item.get("price"))
        quantity = int(order_item.get("quantity"))
        per_item_price = float(item_total_price/quantity)
        
        description = item_name
        
        toppings = order_item.get("toppings")
        topping_description = ""
        if toppings:
            topping_description += ", Toppings: "
            for topping in toppings:
                topping_name = topping["name"]
                if topping_name:
                    if topping == toppings[-1]:
                        topping_description += topping_name
                    else:
                        topping_description += topping_name + ", "
        
        extras_description = ""
        extras = order_item.get("extras")

        if extras:
            extras_description += ", Extras: "
            for add_on in extras:
                add_on_name = add_on["name"]
                if add_on_name:
                    if add_on == extras[-1]:
                        extras_description += add_on_name
                    else:
                        extras_description += add_on_name + ", "
        
        if topping_description:
            description += topping_description
        if extras_description:
            description += extras_description
        if size:
            if size == "S":
                description += ", Size: Small"
            if size == "L":
                description += ", Size: Large"
                
                    
        product_id = "Item_ID_" + str(order_item.get("item"))
        
        
        # try to rerive product from stripe if already in the system, otherwise create a new product
        try:
            product = stripe.Product.retrieve(product_id)
        except stripe.error.InvalidRequestError:
            product = None
            
        if not product:
            attributes = []
            if size:
                attributes.append ("size")
            # creating a new stripe product
            product = stripe.Product.create(
                id = product_id,
                name= item_name,
                attributes = attributes,
            )
        # creating ad-hoc prices (I decided to create ad-hoc pricing due to different sizes and different - add ons)
        price ={
            'unit_amount':int(per_item_price * 100), # covert to cents
            'currency': getattr(settings, "CURRENCY", None),
            'product': product.id,
        }
        
        stripe_price_items.append({"price_data":price, "quantity":quantity, "description":description,})

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items= stripe_price_items,
        mode='payment',
        success_url=getattr(settings, "PAYMENT_SUCCESS_URL", None),
        cancel_url=getattr(settings, "PAYMENT_CANCEL_URL", None),
    )
    context = {
        "STRIPE_PUBLISHABLE_API_KEY":getattr(settings, "STRIPE_PUBLISHABLE_API_KEY", None),
        "CHECKOUT_SESSION_ID":session.id,
    }
    request.session['CHECKOUT_SESSION_ID'] = session.id
    return render(request, "payment.html", context)
 
    
@login_required(login_url='login')
def payment_success(request):
    # when stripe payment is success, it will redirect here
    # TODO :: we need to integrate stripe WEBHOOK before redirect here, since webhook can not setup with local host I havent integrate it yet
    # check session ids are equal
    payment_session_id = request.session['CHECKOUT_SESSION_ID']
    
    session_id_from_url = ""
    try:
        session_id_from_url = request.GET["session_id"]
    except KeyError:
        return render(request, "error.html", {"message": "Invalid request."})
    if payment_session_id != session_id_from_url:
        return render(request, "error.html", {"message": "Invalid request."})
    
    order_items = []
    if 'order_items' in request.session:
        order_items = request.session['order_items']
    else:
        return render(request, "error.html", {"message": "Invalid request."})
    if not order_items:
        return render(request, "error.html", {"message": "Invalid request."})
    order_total = 0.00
    if 'order_total' in request.session:
        order_total = float(request.session['order_total'])
    else:
        return render(request, "error.html", {"message": "Invalid request."})
    
    # saving order to DB
    order = Order()
    order.user = request.user
    order.total = order_total
    order.date_time = datetime.now()
    order.payment = True
    order.payment_session = payment_session_id
    order.save()
    order_id = order.id
    
    
    # saving order items to DB
    for ord_item in order_items:
        order_item = Order_Item()
        order_item.item_name = ord_item.get("item_name")
        size = ord_item.get("size")
        if size:
            order_item.size = size
        
        description = ""
        
        toppings = ord_item.get("toppings")
        topping_description = ""
        if toppings:
            topping_description += "Toppings: "
            for topping in toppings:
                topping_name = topping["name"]
                if topping_name:
                    if topping == toppings[-1]:
                        topping_description += topping_name
                    else:
                        topping_description += topping_name + ", "
        
        extras_description = ""
        extras = ord_item.get("extras")

        if extras:
            extras_description += "Extras: "
            for add_on in extras:
                add_on_name = add_on["name"]
                if add_on_name:
                    if add_on == extras[-1]:
                        extras_description += add_on_name
                    else:
                        extras_description += add_on_name + ", "
        
        if topping_description:
            description = topping_description
        if extras_description:
            description = extras_description
        if description:
            order_item.description = description
        
    
        order_item.quantity =  ord_item.get("quantity")
        order_item.price = float(ord_item.get("price"))
        order_item.order_id = order
        order_item.save()
    
    # remove virtual shopping cart from DB and from session
    shopping_cart = Cart()
    saved_basket = Cart.objects.filter(user_id = request.user.id)
    if saved_basket:
        shopping_cart.id = saved_basket[0].id
        shopping_cart.delete()
    request.session['basket'] = None
    
    # remove other session variables
    request.session['CHECKOUT_SESSION_ID'] = None
    request.session['order_total'] = None
    request.session['order_items'] = None
    
    #save payment details to DB
    return HttpResponseRedirect(reverse("confirmation", args=(order_id,)))


@login_required(login_url='login')
def payment_cancel(request):
    request.session['CHECKOUT_SESSION_ID'] = None
    return HttpResponseRedirect(reverse("cart"))



@login_required(login_url='login')
def confirmation(request, order_id):
    # order confirmation
    order = Order.objects.filter(pk = order_id, user= request.user)
    if not order:
        return render(request, "error.html", {"message": "Invalid order."})
    order_items = Order_Item.objects.filter(order_id = order[0].id)
    if not order_items:
        return render(request, "error.html", {"message": "There are no items in your order"})
    context = {
        "order":order[0],
        "order_items":order_items
    }
    return render(request, "order/confirmation.html", context)