from django.urls import path
from . import views


app_name = 'restaurant'
urlpatterns = [
    
    # URL for Restaurant and User Details 
    path('restaurants/<int:user_id>/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurant_detail/<int:restaurant_id>/<int:user_id>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('profile/<int:user_id>/', views.profile, name="profile"),

    # URL for Bookmark and Visit Status
    path('add_bookmark/<int:restaurant_id>/<int:user_id>/', views.AddBookmark.as_view(), name="add_bookmark"),
    path('remove_bookmark/<int:restaurant_id>/<int:user_id>/', views.RemoveBookmark.as_view(), name="remove_bookmark"),
    path('add_visit/<int:restaurant_id>/<int:user_id>/', views.MarkVisit.as_view(), name="add_visit"),
    path('remove_visit/<int:restaurant_id>/<int:user_id>/', views.UnmarkVisit.as_view(), name="remove_visit"),

    # URL for Reviews
    path('add_review/<int:dish_id>/<int:user_id>/', views.AddReview.as_view(), name="add_review"),
    path('update_review/<int:review_id>/<int:user_id>/', views.UpdateReview.as_view(), name="update_review"),
    path('delete_review/<int:review_id>/<int:user_id>/', views.DeleteReview.as_view(), name="delete_review"),

    # URL for Cart
    path('cart/<int:user_id>/', views.CartView.as_view(), name="cart_list"),
    path('add_cart/<int:dish_id>/<int:user_id>/', views.AddToCart.as_view(), name="add_cart"),
    path('delete_cart/<int:cart_id>/<int:user_id>/', views.DeleteCartItem.as_view(), name="delete_cart"),
    path('update_cart/<int:cart_id>/<int:user_id>/', views.UpdateCartItem.as_view(), name="update_cart"),

    # URL for payment
    path('payment/<pk>/', views.PaymentIntegration.as_view(), name="payment_integration"),
]
