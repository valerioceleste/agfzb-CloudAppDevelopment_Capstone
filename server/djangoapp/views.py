from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_review
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/user_login.html', context)
    else:
            return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = dict()
        context["dealership_list"] = dealerships

        return render(request, "djangoapp/index.html", context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
     if request.method == "GET":
         context = {}
         dealer_url = "http://127.0.0.1:3000/dealerships/get"
         dealer = get_dealer_by_id_from_cf(dealer_url, id = id)
         context['dealer'] = dealer

         review_url = "http://127.0.0.1:5000/api/get_reviews"
         reviews = get_dealer_reviews_from_cf(review_url, id = id)
         context["reviews"] = reviews
         if not context["reviews"] :
            messages.warning(request, "There are no reviews at the moment !!!")   
         return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, id):
    context = {}
    dealer_url = "http://127.0.0.1:3000/dealerships/get"
    
    # Get dealer information
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            car_id = request.POST.get("car")
            
            # Get car information
            car = CarModel.objects.get(pk=car_id)
            
            # Prepare payload for the review
            payload = {
                "time": datetime.utcnow().isoformat(),
                "name": username,
                "dealership": id,
                "id": id,
                "review": request.POST.get("content"),
                "purchase": request.POST.get("purchasecheck") == 'on',
                "purchase_date": request.POST.get("purchasedate"),
                "car_make": car.car_make.name,
                "car_model": car.name,
                "car_year": int(car.year.strftime("%Y"))
            }
            
            # Prepare payload for the API request
            new_payload = {"review": payload}
            review_post_url = "http://127.0.0.1:5000/api/post_review"
            
            # Make the POST request
            post_request(review_post_url, new_payload, id=id)
            
            return redirect("djangoapp:dealer_details", id=id)
        else:
            # Handle the case where the user is not authenticated
            messages.warning(request, "New review not added. Please log in to add a review !!")
            return redirect('djangoapp:index')