from django.contrib import admin

# Register your models here.
from .models import Topping, Regular_Pizza, Sicilian_Pizza, Pasta_salad, Sub, Dinner_Platter, Regular_Pizza_c, Sicilian_Pizza_c, Pasta_salad_c, Sub_c, Dinner_Platter_c, Orders

admin.site.register(Topping)
admin.site.register(Regular_Pizza)
admin.site.register(Sicilian_Pizza)
admin.site.register(Pasta_salad)
admin.site.register(Sub)
admin.site.register(Dinner_Platter)

#customer models.
admin.site.register(Regular_Pizza_c)
admin.site.register(Sicilian_Pizza_c)
admin.site.register(Pasta_salad_c)
admin.site.register(Sub_c)
admin.site.register(Dinner_Platter_c)

#orders.
admin.site.register(Orders)
