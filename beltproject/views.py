from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.

def index (request):
    return render(request, 'logreg.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/travels')

def login(request):
    errors = User.objects.authenticate(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/travels')

def trip_dash (request):
    user=User.objects.get(id=request.session['user_id'])
    context = {
        'user_trips': user.travel_creator.all(),
        'trip': Trip.objects.all()
    }
    return render(request, 'travels.html', context)

def add_new(request):
    return render(request, 'addnew.html')

def create_trip(request):
    errors = Trip.objects.trip_validate(request.POST)
    if len(errors) > 1:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    planner = User.objects.get(id=request.session['user_id'])
    Trip.objects.create(
    destination=request.POST['destination'],
    planner=planner,
    description = request.POST['description'],
    start_date = request.POST['date_from'], 
    end_date = request.POST['date_to']
    )
    return redirect('/travels')

def join(request, trip_id):
    trip=Trip.objects.get(id=trip_id)
    trip.join = True
    trip.save()
    return redirect('/travels')

def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/travels')

def cancel(request, trip_id):
    trip=Trip.objects.get(id=trip_id)
    trip.join = False
    trip.save()
    return redirect('/travels')

def logout(request):
    request.session.flush()
    return redirect('/')

def show_one(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id), 
        }
    return render(request, 'details.html', context)
