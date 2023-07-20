from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models


""" Define a model for Restaurant with the required fields """
class Restaurant(models.Model):
    title = models.CharField(max_length=100)
    cost_for_two = models.DecimalField(max_digits=6, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    address = models.TextField()
    open_timing = models.TimeField()
    close_timing = models.TimeField()
    VEG = 'Veg'
    VEGAN = 'Vegan'
    NON_VEG = 'Non Veg'
    DIETARY_CHOICES = [
        (VEG, 'Vegetarian'),
        (VEGAN, 'Vegan'),
        (NON_VEG, 'Non Vegetarian'),
    ]
    dietary_type = models.CharField(max_length=10, choices=DIETARY_CHOICES, default=NON_VEG,
    )
    
    def __str__(self):
        return self.title


""" Define a model for Cuisine with name field """
class Cuisine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


""" Define a model for Dish with the required fields """
class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cuisines = models.ManyToManyField(Cuisine)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_veg = models.BooleanField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    @property
    def review(self):
        return Review.objects.get(dish=self)
    
    @property
    def cart(self):
        return Cart.objects.get(dish=self)
   
    def __str__(self):
        return self.name


""" Define a model for Review with the required fields """
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        null=True
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email + "__" + self.restaurant.title + "__" + self.dish.name


""" Define a model for Bookmark with the required fields """
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + "__" + self.restaurant.title


""" Define a model for Visit with the required fields """
class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + "__" + self.restaurant.title


""" Define a model for creating a Cart with the required fields """
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.email + "__" + self.dish.name


""" Define a model for Payment with the required fields """
class RazorPay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.email + "__" + self.order_id
