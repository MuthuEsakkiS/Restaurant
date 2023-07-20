from django import forms
from . import models


""" Define a form class for Review """
class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "comment"]


""" Define a form class for add qunatity for dish """
class CartForm(forms.ModelForm):
    class Meta:
        model = models.Cart
        fields = ["quantity"]
