from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import *
from django.views import View
from .models import *
from .forms import *
import razorpay


def profile(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
    }
    return render(request, 'store/profile.html', context)

""" Define a class for list all the available restaurants """
class RestaurantList(View):
    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        """ Apply sorting logic based on the selected option """
        sort_by = self.request.GET.get('sort')
        if sort_by == 'cost_high':
            restaurants = restaurants.order_by('-cost_for_two')
        elif sort_by == 'cost_low':
            restaurants = restaurants.order_by('cost_for_two')
        
        """ Apply filtering logic based on the selected option """
        filter_by = self.request.GET.get('filter')
        data = self.request.GET.get('input')
        if filter_by == 'city' and data:
            restaurants = restaurants.filter(location__icontains=data)
        if filter_by == 'veg' and data:
            restaurants = restaurants.filter(dietary_type__icontains=data)
        context = {
            'restaurants':restaurants,
            'user': user
        }

        return render(request, 'store/restaurant_list.html', context)


""" Define a class to show the detail of a single restaurant """
class RestaurantDetail(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        dishes = Dish.objects.filter(restaurant=restaurant)
        bookmark = Bookmark.objects.filter(restaurant=restaurant, user=user)
        visit = Visit.objects.filter(restaurant=restaurant, user=user)
        cart = Cart.objects.filter(user=user)

        context = {
            'restaurant': restaurant,
            'dishes': dishes,
            'bookmark': bookmark,
            'visit': visit,
            'user_id': user_id,
            'cart': cart
        }
        return render(request, 'store/restaurant_detail.html', context)


""" Define a class to add bookmark to a restaurant """
class AddBookmark(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        user_id = kwargs.get('user_id')
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        Bookmark.objects.get_or_create(restaurant=restaurant, user=request.user)
        return redirect("restaurant:restaurant_detail", restaurant_id=restaurant_id, user_id=user_id)

""" Define a class to remove bookmark from a restaurant """
class RemoveBookmark(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        bookmark = Bookmark.objects.get(user=user)

        if bookmark:
            bookmark.delete()
            return redirect("restaurant:restaurant_detail", restaurant_id=restaurant_id, user_id=user_id)
        else:
            return HttpResponse("Not Bookmarked!")

""" Define a class to mark a visit status of a restaurant """
class MarkVisit(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        user_id = kwargs.get('user_id')
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        Visit.objects.get_or_create(restaurant=restaurant, user=request.user)
        return redirect("restaurant:restaurant_detail", restaurant_id=restaurant_id, user_id=user_id)


""" Define a class to unmark the visit status of a restaurant """
class UnmarkVisit(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        visit = Visit.objects.get(user=user)

        if visit:
            visit.delete()
            return redirect("restaurant:restaurant_detail", restaurant_id=restaurant_id, user_id=user_id)
        else:
            return HttpResponse("Not Visited!")


""" Define a class to add a review for a specific dish """
class AddReview(View):
    def get(self, request, *args, **kwargs):
        dish_id = kwargs.get('dish_id')
        dish = get_object_or_404(Dish, pk=dish_id)
        context = {
            'form': ReviewForm,
            'dish': dish
        }
        return render(request, 'store/review.html', context)

    def post(self, request, *args, **kwargs):
        dish_id = kwargs.get('dish_id')
        user_id = kwargs.get('user_id')
        dish = get_object_or_404(Dish, pk=dish_id)
        user = get_object_or_404(User, pk=user_id)

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(user=user, restaurant=dish.restaurant, dish=dish, rating=rating, comment=comment)
        return redirect('restaurant:restaurant_detail', restaurant_id=dish.restaurant.id, user_id=user_id)


""" Define a class to delete a review from a specific dish """
class DeleteReview(View):
    def get(self, request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        user_id = kwargs.get('user_id')
        review = get_object_or_404(Review, pk=review_id)

        restaurant_id = review.dish.restaurant.id
        review.delete()
        return redirect('restaurant:restaurant_detail', restaurant_id=restaurant_id, user_id=user_id)

""" Define a class to update a review """
class UpdateReview(View):
    def get(self, request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        context = {
            'form': ReviewForm,
            'review': review
        }
        return render(request, 'store/review.html', context)
         
    def post(self, request, *args, **kwargs):
        review_id = kwargs.get('review_id')
        user_id = kwargs.get('user_id')
        review = get_object_or_404(Review, pk=review_id)
        dish = review.dish

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review.rating = rating
        review.comment = comment
        review.save()
        return redirect('restaurant:restaurant_detail', restaurant_id=dish.restaurant.id, user_id=user_id)

""" Function to calculate the total amount from the dish listed in the cart """
def amount_calculation(items):
    total_amount = 0
    for item in items:
        total_amount = total_amount + (item.quantity * item.dish.price)
    return total_amount

""" List all the dishes in the cart """
class CartView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = amount_calculation(items=cart_items)
        context = {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'user_id': user_id
        }
        return render(request, 'store/cart.html', context)

""" Add a dish to the cart """
class AddToCart(View):
    def get(self, request, *args, **kwargs):
        dish_id = kwargs.get('dish_id')
        dish = get_object_or_404(Dish, pk=dish_id)
        context = {
            'dish': dish,
            'form': CartForm
        }
        return render(request, 'store/add_dish.html', context)
    
    def post(self, request, *args, **kwargs):
        dish_id = kwargs.get('dish_id')
        user_id = kwargs.get('user_id')
        dish = get_object_or_404(Dish, pk=dish_id)
        user = get_object_or_404(User, pk=user_id)

        quantity = request.POST.get('quantity')
        Cart.objects.create(user=user, dish=dish, quantity=quantity)
        return redirect('restaurant:cart_list', user_id=user_id)

""" Update the quantity of dish in the cart """
class UpdateCartItem(View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)
        context = {
            'cart': cart,
            'form': CartForm
        }
        return render(request, 'store/add_dish.html', context)
    
    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)
        user_id = kwargs.get('user_id')

        quantity = request.POST.get('quantity')
        cart.quantity = quantity
        cart.save()
        return redirect('restaurant:cart_list', user_id=user_id)

""" Delete the dish from the cart """
class DeleteCartItem(View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)
        user_id = kwargs.get('user_id')
        cart.delete()
        return redirect('restaurant:cart_list', user_id=user_id)

""" Define a class for payment integration using Razorpay """
class PaymentIntegration(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cart_items = Cart.objects.all()
        amount = amount_calculation(items=cart_items)
        amount_in_paise = int(amount * 100)
        
        client = razorpay.Client(auth=("rzp_test_9KTasL8waDWWUZ", "qDiBsEFapP9XV9MPwstEZg6b"))
        payment = client.order.create({'amount': amount_in_paise, 'currency': 'INR', 'payment_capture': '1'})
        razor_pay = RazorPay(user=request.user, total_amount=amount, order_id=payment['id'])
        razor_pay.save()
        context = {
            'cart_items': cart_items,
            'total_amount': amount,
            'payment': payment,
            'user_id': user_id,
        }
        return render(request, 'store/cart.html', context)
