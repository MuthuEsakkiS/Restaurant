from django.urls import path
from . import views


app_name = "authentication"
urlpatterns = [
    
    # URL for sign-up, sign-in and sign-out process
    path('', views.Signin.as_view(), name='sign_in'),
    path('signup', views.Signup.as_view(), name="sign_up"),
    path('signout', views.signout, name='sign_out'),

    # URL for delete account, user list, import and export user data
    path('delete_user/<int:user_id>/', views.DeleteUser.as_view(), name="delete_user"),
    path('user_list', views.user_list, name='user_list'),
    path('export_to_excel', views.ExportToExcel.as_view(), name='export_to_excel'),
    path('import_from_excel', views.ImportFromExcel.as_view(), name="import_from_excel"),
]
