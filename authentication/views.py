from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import *
from . import forms
import pandas
from django.utils import timezone


""" Define a class for sign-up process """
class Signup(View):
    def get(self, request):
        context = {
            'form': forms.SignupForm
        }
        return render(request, 'authentication/signup.html', context)

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:   
                user = User.objects.create_user(username=username, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('authentication:sign_in')
            except:
                return render(request, 'authentication/warning.html', {'same_email': 'same_email'})
        else:
            return render(request, 'authentication/warning.html', {'passcode_check': 'passcode_check'})


""" Define a class for sign-in process """
class Signin(View):
    def get(self, request):
        return render(request, 'authentication/signin.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('restaurant:restaurant_list', user_id=user.id)
        else:
            return render(request, 'authentication/warning.html', {'incorrect_login': 'incorrect_login'})


""" Define a function for sign-out process """
def signout(request):
    logout(request)
    return redirect('authentication:sign_in')


""" Define a class to delete the user account permanently """
class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        try:
            user.delete()
            return render(request, 'authentication/warning.html', {'delete_user': 'delete_user'})
        except User.DoesNotExist:
            return render(request, 'authentication/warning.html', {'doesnot_exist': 'doesnot_exist'})


""" Define a function to display all the user """
def user_list(request):
    users = User.objects.filter(is_staff=False)
    context = {
        'users': users,
    }
    return render(request, 'authentication/user_list.html', context)


""" Define a class to do export functionality """
class ExportToExcel(View):
    def get(self, request):
        users = User.objects.filter(is_staff=False).values('username', 'first_name', 'last_name', 'date_joined')
        data_frame = pandas.DataFrame(list(users))
        data_frame['date_joined'] = data_frame['date_joined'].dt.tz_convert('Asia/Kolkata')
        data_frame['date_joined'] = data_frame['date_joined'].dt.tz_localize(None)
        writer = pandas.ExcelWriter('user_list.xlsx')
        data_frame.to_excel(writer, index=False)
        writer.close()

        with open('user_list.xlsx', 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=user_list.xlsx'
            return response


class UploadToDatabase:
    pass
