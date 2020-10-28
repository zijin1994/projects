from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("shoppingcart", views.shopping_cart_view, name="shoppingcart"),
    path("logout", views.logout_view, name="logout"),
    path("pizza", views.pizza_view, name="pizza"),
    path("<str:title>/<str:name>/<str:size>/pizza", views.add_pizza_view, name="add_pizza"),
    path("<str:title>/<str:name>/<str:size>/pizza/toppings", views.toppings_view, name="toppings"),
    path("subs", views.subs_view, name="subs"),
    path("<str:name>/<str:size>/subs", views.add_sub_view, name="add_sub"),
    path("<str:sub_name>/<str:sub_size>/subs/sub_toppings", views.sub_toppings_view, name="sub_toppings"),
    path("pasta_and_salad", views.pasta_and_salad_view, name="pasta_and_salad"),
    path("pasta_and_salad/<int:id>", views.add_pasta_and_salad_view, name="add_pasta_and_salad"),
    path("dinner_platter", views.dinner_platter_view, name="dinner_platter"),
    path("dinner_platter/<int:id>", views.add_dinner_platter_view, name="add_dinner_platter"),
    path("confirm_items", views.confirm_items_view, name="confirm_items")

]
