# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from bizzbuzz.models import Preferences
from bizzbuzz.models import News
from bizzbuzz.forms import PrefForm
import time
# from .models import Register


def index_view(request):
    return render(request,'bizzbuzz/index.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'bizzbuzz/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # if request.user.is_authenticated:
        #     messages.error(request, 'This account is already logged in')
        #     return render(request, 'bizzbuzz/login.html')

        if user:    #gets username and password, logs the user in
            login(request, user)
            #if they've never logged in before, go to select channels
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'bizzbuzz/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'bizzbuzz/signup.html')
    elif request.method == 'POST':
        if request.POST.get('username') and request.POST.get('password'):
            #gets the fields from the form in signup.html and puts into database
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, None, password)
                user.save()

                preference = Preferences(username=username)
                preference.save()
                #run 'SELECT * from auth_user' in query console to see contents of this table
                return redirect('login')
            else:
                messages.error(request, 'Username is already taken')
                return render(request, 'bizzbuzz/signup.html')
        else:
            messages.error(request, 'Please enter a valid username and password')
            return render(request, 'bizzbuzz/signup.html')

# def forgotpassword_view(request):
#     return render(request,'bizzbuzz/forgotpassword.html')
#
# def searchchannel_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     return render(request,'bizzbuzz/searchchannel.html', {'name': request.user.username})

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    #gather user's preferences to use in search later
    username = request.user.username
    preference = Preferences.objects.get(username=username)
    companies = ['apple', 'google', 'facebook', 'microsoft']
    if request.method == 'GET':
        preferred = []
        for i in companies: #gets the current values of each company, puts in appropriate list, and passes lists to HTML
            value = getattr(preference, i)
            if value is True:
                preferred.append(i.upper())

    titles= []
    urls = []
    summaries = []
    indices = []
    sources = []
    i = 1

    for pref in preferred:
        #filter articles containing relevant company name
        news = News.objects.filter(title__icontains=pref)
        #hard coded 'applebee's' exception, can make more generic if other exceptions arise
        if pref.lower() == 'apple':
            news=news.exclude(title__icontains="applebee's")
        for n in news:
            #check for duplicate urls
            if getattr(n, 'url') not in urls:
                titles.append(getattr(n, 'title'))
                urls.append(getattr(n, 'url'))
                summaries.append(getattr(n, 'summary'))
                indices.append(i)
                i+=1
                #update with extra sources once we implement them
                if 'forbes.com' in getattr(n, 'url').lower():
                    sources.append('FORBES')
                else:
                    sources.append('BI')
    #zip together titles, urls, summaries, sources, and send to home.html
    return render(request, 'bizzbuzz/home.html', {'name': username, 'articles' : zip(titles, urls, summaries, sources, indices)})

def selectchannel_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    username = request.user.username
    preference = Preferences.objects.get(username=username) #.values_list('apple', 'microsoft', 'google', 'facebook')
    companies = ['apple', 'google', 'facebook', 'microsoft']
    if request.method == 'GET':
        preferred = []
        not_preferred = []
        i = 0
        for i in companies: #gets the current values of each company, puts in appropriate list, and passes lists to HTML
            value = getattr(preference, i)
            if value is False:
                not_preferred.append(i.upper())
            else:
                preferred.append(i.upper())
        # print(preferred)
        # print(not_preferred)
        return render(request,'bizzbuzz/selectchannel.html', {'name': request.user.username, 'preferred': preferred, 'not_preferred': not_preferred})
    elif request.method == 'POST':
        # print("IN POST")
        MyPrefForm = PrefForm(request.POST)
        changePref = Preferences.objects.get(username=username)
        preferred = []
        not_preferred = []
        if MyPrefForm.is_valid():
            if "apple" in request.POST:
                current = changePref.apple
                new = not current
                changePref.apple = new
                changePref.save()
            if "microsoft" in request.POST:
                current = changePref.microsoft
                new = not current
                changePref.microsoft = new
                changePref.save()
            if "facebook" in request.POST:
                current = changePref.facebook
                new = not current
                changePref.facebook = new
                changePref.save()
            if "google" in request.POST:
                current = changePref.google
                new = not current
                changePref.google = new
                changePref.save()
        i = 0
        for i in companies:
            print(i)
            value = getattr(preference, i)
            print(value)
            if value is False:
                not_preferred.append(i.upper())
            else:
                preferred.append(i.upper())

        return render(request, 'bizzbuzz/selectchannel.html', {'name': request.user.username, 'preferred': preferred, 'not_preferred': not_preferred})