from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import *
from . import forms
import pandas


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

        try:   
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect('authentication:sign_in')
        except:
            return render(request, 'authentication/warning.html', {'same_email': 'same_email'})


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
@login_required
def signout(request):
    logout(request)
    return redirect('authentication:sign_in')


""" Define a class to delete the user account permanently """
class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        try:
            user.delete()
            return render(request, 'authentication/warning.html', {'delete_user': 'delete_user'})
        except User.DoesNotExist:
            return render(request, 'authentication/warning.html', {'doesnot_exist': 'doesnot_exist'})


""" Define a function to display all the user """
@login_required
def user_list(request):
    users = User.objects.filter(is_staff=False)
    context = {
        'users': users,
    }
    return render(request, 'authentication/user_list.html', context)


""" Define a class to do export functionality """
class ExportToExcel(LoginRequiredMixin, View):
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


""" Define a class to import data from Excel to Database """
class ImportFromExcel(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'authentication/import_excel.html')

    def post(self, request):
        file = request.FILES['myfile']
        file_path = "/Users/esakkimuthu/Downloads/{}".format(file.name)
        excel_data = pandas.read_excel(file_path)
        data_frame = excel_data
        for data_frame in data_frame.itertuples():
            if not User.objects.filter(username = data_frame.email).exists():
                user_object = User.objects.create(username=data_frame.email, 
                                                      password=make_password(str(data_frame.password)), 
                                                      first_name=data_frame.first_name, 
                                                      last_name=data_frame.last_name)
                user_object.save()
        return render(request, 'authentication/import_excel.html', {'success': 'success'})
