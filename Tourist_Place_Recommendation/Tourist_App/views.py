from django.shortcuts import redirect, render, reverse
from Tourist_App.models import *
import ast
from Tourist_App import read_dataset
from Tourist_App import rawQuery
from django.utils import timezone
from rest_framework.decorators import api_view  # type: ignore
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import timezone
from django.http import JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

import os


def index(request):
    return render(request, "login.html")


def logoutNow(request):
    logout(request)
    return render(request, "user/login.html")


def user(request):
    return render(request, "user/login.html")


def registration(request):
    return render(request, "user/registration.html")


from django.contrib.auth import authenticate, login


def saveUser(request):
    if request.method == "POST":
        name = request.POST["uname"]
        contactNo = request.POST["contactNo"]
        emailId = request.POST["emailId"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        username = request.POST["username"]
        password = request.POST["password"]
        category_prefs = request.POST.getlist("category")
        location_prefs = request.POST.getlist("location")
        print(category_prefs)
        user1 = User.objects.filter(
            contact=contactNo, email=emailId, is_verified=1
        ).first()
        if user1 is not None:
            messages.error(request, "Duplicate found...")
            return redirect("reg")

        user2 = User.objects.filter(
            contact=contactNo, email=emailId, is_verified=0
        ).first()
        if user2 is not None:

            user2.name = name
            user2.address = address
            user2.gender = gender
            user2.user_name = username
            user2.password = password

            user2.save()
            id = user2.id
            phone = user2.contact

        if (
            User.objects.filter(email=emailId).exists()
            or User.objects.filter(contact=contactNo).exists()
        ):
            messages.error(request, "Duplicate found.... Testing")
            return redirect("reg")

        user = User.objects.create_user(
            email=emailId,
            name=name,
            password=password,
            contact=contactNo,
            address=address,
            user_name=username,
            gender=gender,
            category_prefs=str(category_prefs),
            location_prefs=str(location_prefs),
        )
        user.save()
        messages.success(request, "Registration Successful...!")
        return redirect("userLogin")

    return render(request, "user/registration.html")


# @login_required(login_url="/user/")
def home(request):
    return render(request, "user/home.html")


def userlogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, user_name=username, password=password)
        if user == None:
            return render(
                request, "user/login.html", {"error": "Invalid login credentials"}
            )
        if user != None:
            if user.is_verified == 0:
                return render(
                    request, "user/login.html", {"error": "Invalid login credentials"}
                )
        login(request, user)
        request.session["userid"] = user.id  # type: ignore
        request.session["userName"] = user.name
        # Check if the dataset needs to be loaded (only for admin users, for example)
        if user.is_superuser and not DatasetLoaded.objects.filter(is_loaded=True).exists():
            loadData(request)
        messages.success(request, "Login successfully...")
        return redirect("home")
    else:
        return render(request, "user/login.html")


from .models import User, Review


@login_required(login_url="/user/")
@csrf_exempt
def preferences(request):
    if request.method == "POST":
        values = request.POST.getlist("values[]")
        user = User.objects.get(pk=request.user.id)
        if values:
            user.category_prefs = str(values)
            print("test4", str(values))
            print(user.category_prefs)
            user.save()
            data = rawQuery.get_data(values)
            return JsonResponse(list(data), safe=False)
        else:
            return JsonResponse({"error": "No checkboxes selected"}, status=400)
    else:
        return render(request, "user/preferences.html")


from Tourist_App.recommend import recommend


@login_required(login_url="/user/")
@csrf_exempt
def get_recommendation(request):
    if request.method == "GET":
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        user_ratings = Review.objects.filter(user=user)
        user_ratings_with_place_ids = user_ratings.values("place_id", "rating")

        new_user_data = {
            "user_id": user_id,
            "place_ratings": {item["place_id"]: item["rating"] for item in user_ratings_with_place_ids},
            "category_preferences": ast.literal_eval(user.category_prefs),
            "location_preferences": ast.literal_eval(user.location_prefs),
        }

        reclist = recommend(new_user_data)

        data = []
        for place_name in reclist:
            data += rawQuery.get_data_test(place_name)

        return JsonResponse(data, safe=False)


@login_required(login_url="/user/")
@csrf_exempt
def recommendation(request):
    return render(request, "user/recommendation.html")


@login_required(login_url="/user/")
def profile(request):
    user_id = request.session["userid"]
    user = User.objects.filter(id=user_id).first()
    return render(request, "user/profile.html", {"user": user})


@login_required(login_url="/user/")
def search(request):
    return render(request, "user/search.html")


@login_required(login_url="/user/")
def editProfile(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        user_name = request.POST["username"]
        current_password = request.POST["currentPassword"]
        new_password = request.POST["newPassword"]
        confirm_new_password = request.POST["confirmNewPassword"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        location_prefs = request.POST.getlist("location")

        if check_password(current_password, user.password):
            user.name = name
            user.contact = phone
            user.email = email
            user.user_name = user_name
            user.gender = gender
            user.address = address
            user.location_prefs = str(location_prefs)

            if new_password and new_password == confirm_new_password:
                user.password = make_password(new_password)
                messages.success(request, "Password updated successfully.")
            elif new_password or confirm_new_password:
                messages.error(request, "New passwords do not match.")
                return render(request, "user/profile.html", {"user": user})

            user.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Current password is incorrect.")

        return render(request, "user/profile.html", {"user": user})
    else:
        return render(request, "user/profile.html", {"user": user})


def feedback(request):
    return render(request, "user/ratings.html")


def loadData(request):
    if not DatasetLoaded.objects.filter(is_loaded=True).exists():
        result = read_dataset.import_csv_data()
        if result:
            messages.success(request, 'Data Loaded successfully...')
            response_data = {"closeModal": True}
        else:
            messages.error(request, 'Data Loading failed...')
            response_data = {"closeModal": False}
    else:
        messages.info(request, 'Data already loaded.')
        response_data = {"closeModal": True}

    return JsonResponse(response_data)


def feedback(request):
    return render(request, "user/ratings.html")


def kelvin_to_celsius(kelvin_temp):
    celsius_temp = kelvin_temp - 273.15
    return round(celsius_temp, 2)


from django.http import HttpResponse
from PIL import Image
import io
import base64


def getMoreDetails(request, id):
    details = Dataset.objects.filter(ID=id).first()
    user_id = request.user.id
    place_id = id
    rating_count = rawQuery.get_review_counts(id)
    review_details = rawQuery.get_user_review(id)
    Isreviewed = rawQuery.has_user_reviewed(user_id, id)
    print("rating count---->", rating_count)
    print("review details---->", review_details)
    print("has_reviewe------->", Isreviewed)
    print("City :", details.City)
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": details.City,
        "appid": "8018adbb3f533582a7a5ccc7f533fab3",
        "units": "metric",
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    print("Weather Data:", weather_data)

    return render(
        request,
        "user/place_details.html",
        {
            "place_id": place_id,
            "details": details,
            "weather_data": weather_data,
            "rating_count": json.dumps(rating_count),
            "review_details": json.dumps(review_details),
            "Isreviewed": Isreviewed,
        }
    )


def search_places(request):
    query = request.GET.get("query", "")
    print(query)
    name = "%" + query + "%"
    data = rawQuery.get_search_data(name)
    return JsonResponse(list(data), safe=False)


@login_required(login_url="/user/")
def topRated(request):
    data = rawQuery.get_top_data()
    return render(request, "user/top_rated.html", {"data": data})


def add_favorite(request):
    if request.method == "POST":
        user_id = request.user.id
        place_id = request.POST["place_id"]

        favorite = Favorite.objects.filter(user_id=user_id, place_id=place_id).first()

        if favorite is None:
            favorite = Favorite(user_id=user_id, place_id=place_id)
            favorite.save()
            # Optionally, you can add a success message
        else:
            # Optionally, you can add a message indicating that the place is already a favorite
            pass

    return redirect("home")  # Redirect to user home after adding favorite


from django.http import JsonResponse
from .models import Review  # Import your Review model
from django.db import transaction
from .models import Review, ReviewPhoto


def submit_review(request, id):
    if request.method == "POST":
        # Extract form data
        rating = request.POST.get("rating")
        with_whom = request.POST.get("with_whom")
        review_text = request.POST.get("reviewText")

        # Validate form data
        if not rating or not review_text:
            return JsonResponse(
                {"error": "Rating and review text are required."}, status=400
            )

        user_id = request.session.get("userid")
        place_id = id

        review = Review.objects.create(
            user_id=user_id,
            place_id=place_id,
            rating=rating,
            with_whom=with_whom,
            review_text=review_text,
            # Add any other fields you have in your Review model
        )

        uploaded_files = request.FILES.getlist("images")

        from django.conf import settings

        upload_dir = os.path.join(
            settings.MEDIA_ROOT, f"review_images/{user_id}/{place_id}"
        )
        os.makedirs(upload_dir, exist_ok=True)

        for file in uploaded_files:
            file_name = file.name
            file_path = os.path.join(upload_dir, file_name)

            # Ensure unique filenames
            counter = 1
            while os.path.exists(file_path):
                name, extension = os.path.splitext(file_name)
                file_name = f"{name}_{counter}{extension}"
                file_path = os.path.join(upload_dir, file_name)
                counter += 1

            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Create ReviewPhoto object
            ReviewPhoto.objects.create(
                review=review, photo=f"review_images/{user_id}/{place_id}/{file_name}"
            )

        return JsonResponse(
            {
                "success": True,
                "redirect_url": reverse("getMoreDetails", kwargs={"id": id}),
            }
        )

    return JsonResponse({"error": "Invalid request method"}, status=400)


def remove_favorite(request):
    if request.method == "POST":
        user_id = request.user.id
        place_id = request.POST["place_id"]

        favorite = Favorite.objects.filter(user_id=user_id, place_id=place_id).first()

        if favorite is not None:
            favorite.delete()
            # Optionally, you can add a success message
        else:
            # Optionally, you can add a message indicating that the place is not a favorite
            pass

    return redirect("home")  # Redirect to user home after removing favorite


from django.contrib.auth.decorators import login_required


@login_required
def get_user_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    favorite_ids = [favorite.place_id for favorite in favorites]
    return JsonResponse({"userFavorites": favorite_ids})


@login_required
def favorite_places(request):
    print("request------------->", request.user.id)
    user = request.user
    if user.is_authenticated:
        favorite_places_ids = Favorite.objects.filter(user_id=user.id).values_list(
            "place_id", flat=True
        )
        data = rawQuery.get_fav_data(user)
        return render(request, "user/favorite_places.html", {"data": data})
