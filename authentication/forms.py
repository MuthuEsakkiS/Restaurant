from django import forms


""" Define a class for Sign-up form to create an account """
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=8, min_length= 1, required=True, widget=forms.PasswordInput(attrs={'placeholder':'Length should not exceed 8.'}))
