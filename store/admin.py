from django.contrib import admin
from . import models

""" List the models should present in the admin panel """
myModels = [models.Restaurant, models.Cuisine, models.Dish, models.RazorPay]
admin.site.register(myModels)
