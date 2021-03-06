from django.shortcuts import render,redirect
# from .models import details
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UserName
from django.contrib.auth import authenticate, login, logout
from .models import FriendDetails
import requests
from bs4 import BeautifulSoup
# Create your   views here.
def del_request(request, user_name):
    if request.user.is_authenticated:
        user = request.user
    bro = FriendDetails.objects.get(friend_user_name=user_name)
    bro.user.remove(user)
    return redirect("/main/")
def refresh(request, user_name):
    url = f"https://www.codechef.com/users/{user_name}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    name = str(soup.findAll('h2')[1]).strip('<h2/>')
    table = soup.find('div', attrs = {'class':'rating-number'})
    rat = soup.find('span', attrs={'class':'rating'})
    num = int(rat.text[0])
    rat = (rat.text[1] + " ")*num
    print(rat)
    if table is not None:
        table = table.text
    detail = FriendDetails.objects.get(friend_user_name=user_name)
    detail.friend_name = name
    detail.rating = table
    detail.stars = rat
    detail.save()
    return redirect("/main/")
def home(request):
    bro = {}
    if request.user.is_authenticated:
        user = request.user
        bro = user.frienddetails_set.all()
    if request.method == "POST":
        form = UserName(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            bro = FriendDetails.objects.filter(friend_user_name=user_name).first()
            if bro is not None:
                bro.user.add(user)
                bro = FriendDetails.objects.filter(friend_user_name=user_name).values()
                return(render(request, 'main/home.html', context={'bro':user.frienddetails_set.all(),'form':form}))
            else:
                url = f"https://www.codechef.com/users/{user_name}"
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html5lib')
                name = str(soup.findAll('h2')[1]).strip('<h2/>')
                table = soup.find('div', attrs = {'class':'rating-number'})
                rat = soup.find('span', attrs={'class':'rating'})
                num = int(rat.text[0])
                rat = (rat.text[1] + " ")*num
                if table is not None:
                    table = table.text
                    bro = FriendDetails(friend_name=name, friend_user_name=user_name, rating=table, stars=rat)
                    bro.save()
                    bro.user.add(user)
                    return(render(request, 'main/home.html', context={'bro':user.frienddetails_set.all(),'form':form}))
                else:
                    messages.error(request, f"{user_name} is not a valid Username")
    form = UserName
    # email = details.objects.all
    # template = loader.get_template('/index.html')
    # context = {'email': email}
    return render(request, 'main/home.html', {'form':form, 'bro':bro})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, f"User {user_name} created successfully")
            return redirect("/main/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg} : {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = SignUpForm
    return(render(request, 'main/register.html', context={'form':form}))

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/main/")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(user_name, password)
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                messages.success(request, "You are now logged in !")
                login(request, user)
                return redirect("/main/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm
    return(render(request, "main/login.html", context={'form':form}))
