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
    
