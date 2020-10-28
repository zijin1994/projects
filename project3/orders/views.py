from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from decimal import *
from .models import *
order_history = []
shopping_cart = {}
current_making = {}

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/user.html", context)

#login and register.
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first name"]
    last_name = request.POST["last name"]
    email = request.POST["email"]
    if "action_login" in request.POST:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if the user does not have a shopping_cart, create one.
            if user.username not in shopping_cart:
                shopping_cart[user.username]={"orders":[], "totalprice": 0}
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})

    elif "action_register" in request.POST:
        if username and email and password and first_name and last_name:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            #init a shoppingcart.
            shopping_cart[user.username]={"orders":[], "totalprice": 0}

            return render(request, "orders/login.html", {"message": "Register success."})
        else:
            return render(request, "orders/login.html", {"message": "Need all the info to register."})

#pizzas.
def pizza_view(request):
    #display pizza menu.
    context = {
          "regular_pizza": Regular_Pizza.objects.all(),
          "sicilian_pizza": Sicilian_Pizza.objects.all()
      }
    return render(request, "orders/pizza.html", context)

def add_pizza_view(request, title, name, size):
    #find that pizza in database.
    if "%20" in name:
        name = name.replace("%20", " ")
    if "Regular" in title:
        pizza = Regular_Pizza.objects.get(name=name, size=size)
        new_pizza = Regular_Pizza_c(size=pizza.size, price=pizza.price, name=pizza.name)
        new_pizza.save()
    elif "Sicilian" in title:
        pizza = Sicilian_Pizza.objects.get(name=name, size=size)
        new_pizza = Sicilian_Pizza_c(size=pizza.size, price=pizza.price, name=pizza.name)
        new_pizza.save()

    current_making[request.user.username]=new_pizza
    if "1" in name:
        topping_number = 1
    elif "2" in name:
        topping_number = 2
    elif "3" in name:
        topping_number = 3
    elif "Special" in name:
        topping_number = 5
    else:
        topping_number = 0

    context = {
        "name":new_pizza.name,
        "topping_number": topping_number,
        "toppings": Topping.objects.all(),
        "title": new_pizza,
        "size":new_pizza.size
    }
    return render(request, "orders/buildpizza.html", context)

def toppings_view(request, title, name, size):
    #add selected toppings.
    toppings = Topping.objects.all()
    pizza = current_making[request.user.username]
    toppinglist = request.POST.getlist("topping", [])
    for topping in toppings:
        if topping.name in toppinglist:
            pizza.toppings.add(topping)
    shopping_cart[request.user.username]["orders"].append(pizza)
    del current_making[request.user.username]
    return render(request, "orders/message.html", {"message": "Added to shoppingcart."})

#subs.
def subs_view(request):
    #display subs menu.
    context = {
          "subs": Sub.objects.all()
    }
    return render(request, "orders/sub.html", context)

def add_sub_view(request, name, size):
    #find subs.
    if "%20" in name:
        name = name.replace("%20", " ")
    sub = Sub.objects.get(name=name, size=size)
    new_sub = Sub_c(size=sub.size, name=sub.name, price=sub.price)
    new_sub.save()

    current_making[request.user.username]=new_sub
    toppinglist = []
    mushrooms = Topping.objects.get(name="Mushrooms")
    greenpeppers = Topping.objects.get(name="Green Peppers")
    onions = Topping.objects.get(name="Onions")
    toppinglist.append(mushrooms)
    toppinglist.append(greenpeppers)
    toppinglist.append(onions)

    context = {
        "name":new_sub.name,
        "toppings":toppinglist,
        "title": new_sub,
        "size":new_sub.size
    }
    return render(request, "orders/buildsub.html", context)

def sub_toppings_view(request, sub_name, sub_size):
    #add selected toppings or extra cheese to subs.
    toppings = Topping.objects.all()
    sub = current_making[request.user.username]
    for topping in toppings:
        if topping.name in request.POST:
            sub.toppings.add(topping)
            sub.price = sub.price + Decimal(0.5)
            sub.save()
    if "cheese" in request.POST:
        sub.price = sub.price + Decimal(0.5)
        sub.name = sub.name + " with extra cheese"
        sub.save()
    shopping_cart[request.user.username]["orders"].append(sub)
    del current_making[request.user.username]
    return render(request, "orders/message.html", {"message": "Added to shoppingcart."})

#pasta and salad.
def pasta_and_salad_view(request):
    #find pasta_salad in database.
    context = {
        "pasta_and_salad":Pasta_salad.objects.all()
    }
    return render(request, "orders/pasta_and_salad.html", context)

def add_pasta_and_salad_view(request, id):
    #add to shoppingcart.
    item = Pasta_salad.objects.get(id=id)
    new_item = Pasta_salad_c(name=item.name, price=item.price)
    new_item.save()
    shopping_cart[request.user.username]["orders"].append(new_item)
    return render(request, "orders/message.html", {"message": "Added to shoppingcart."})

#dinner platters.
def dinner_platter_view(request):
    #find dinner platter in database.
    context = {
        "dinner_platter": Dinner_Platter.objects.all()
    }
    return render(request, "orders/dinner_platter.html", context)

def add_dinner_platter_view(request, id):
    #add to shoppingcart.
    item = Dinner_Platter.objects.get(id=id)
    new_item = Dinner_Platter_c(id=item.id, size=item.size, name=item.name, price=item.price)
    new_item.save()
    shopping_cart[request.user.username]["orders"].append(new_item)
    return render(request, "orders/message.html", {"message": "Added to shoppingcart."})

#shoppingcart and confirm orders.
def shopping_cart_view(request):
    #display shoppingcart with totalprice.
    total_price = 0
    for item in shopping_cart[request.user.username]["orders"]:
        total_price = total_price+item.price
    shopping_cart[request.user.username]["totalprice"] = total_price
    context = {
        "user": request.user,
        "orders": shopping_cart[request.user.username]["orders"],
        "total": total_price
    }
    return render(request, "orders/shoppingcart.html", context)

#get customer orders and put in database.
def confirm_items_view(request):
    order_list = {}
    for food in shopping_cart[request.user.username]["orders"]:
        if str(food) not in order_list:
                order_list[str(food)]=[]
        if hasattr(food, "toppings"):
            topping_string_list = []
            for t in food.toppings.all():
                topping_string_list.append(str(t))
            order_list[str(food)].append(topping_string_list)
    order = Orders(customer_name=request.user.username, price=shopping_cart[request.user.username]["totalprice"])
    order.setdishes(order_list)
    order.save()
    for item in shopping_cart[request.user.username]["orders"]:
        item.delete()
    shopping_cart[request.user.username]["orders"] = []
    send_mail(
    f"Order confirmation for order {order.id}",
    f"Dear {request.user.first_name} {request.user.last_name}:   You have successfully ordered from pinocchiospizza!",
    "zijin@ualberta.ca",
    [request.user.email],
    fail_silently=False,
    )
    shopping_cart[request.user.username]["totalprice"] = 0
    return render(request, "orders/message.html", {"message": "Order has been placed."})




def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
