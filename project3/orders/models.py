from django.db import models
import json

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Regular_Pizza(models.Model):
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Regular Pizza ------- {self.price}"

class Sicilian_Pizza(models.Model):
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Sicilian Pizza ------- {self.price}"

class Pasta_salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} ------ {self.price}"

class Sub(models.Model):
    size = models.CharField(max_length=5)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Sub ------ {self.price} (Add toppings +0.50 each)"

class Dinner_Platter(models.Model):
    size = models.CharField(max_length=5)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.name} Dinner Platter ------ {self.price}"

#customer models.

class Regular_Pizza_c(models.Model):
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Regular Pizza ------- {self.price}"

class Sicilian_Pizza_c(models.Model):
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    name = models.CharField(max_length=64)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Sicilian Pizza ------- {self.price}"

class Pasta_salad_c(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} ------ {self.price}"

class Sub_c(models.Model):
    size = models.CharField(max_length=5)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return f"{self.size} {self.name} Sub ------ {self.price} (Add toppings +0.50 each)"

class Dinner_Platter_c(models.Model):
    size = models.CharField(max_length=5)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.size} {self.name} Dinner Platter ------ {self.price}"

#orders.
class Orders(models.Model):
    customer_name = models.CharField(max_length=64)
    dishes = models.CharField(max_length=1024, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def setdishes(self, x):
        self.dishes = json.dumps(x)

    def getdishes(self):
        return json.loads(self.dishes)

    def __str__(self):
        return f"{self.customer_name}'s order ------ {self.price}"
