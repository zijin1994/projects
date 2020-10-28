import pycountry
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import *

# Create your views here.
def index(request):
      if not request.user.is_authenticated:
          return render(request, "matches/login.html", {"message": None})
      context = {
          "user": User_info.objects.get(username=request.user.username)
      }
      return render(request, "matches/user.html", context)

#login.
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    if "action_login" in request.POST:
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "matches/login.html", {"message": "Invalid username or password, try again!"})
        else:
            return render(request, "matches/login.html", {"message": "username or password is missing, try again!"})

    elif "action_register" in request.POST:
        if not (username or password):
            return render(request, "matches/register.html")
        else:
            context = {
                "username": username,
                "password": password
            }
            return render(request, "matches/register.html", context)

#register.
def register_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first name"]
    last_name = request.POST["last name"]
    email = request.POST["email"]

    if username and email and password and first_name and last_name:
        #check if username is unique.
        existing_users = User_info.objects.all()
        for user in existing_users:
            if user.username == username:
                return render(request, "matches/register.html", {"message": "That username has already been used."})

        #create user in database.
        new_user = User_info(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        new_user.save()
        #create user in django built-in app form.
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        return render(request, "matches/login.html", {"message": "Register success."})
    else:
        return render(request, "matches/register.html", {"message": "Need all the info to register."})

#task_bar.
def task_bar_view(request):
    user = User_info.objects.get(username=request.user.username)

    #complete info.
    if "action_complete_info" in request.POST:

        context = {
            "user": request.user,
            "countries": pycountry.countries,
            "educations": Education.objects.all(),
            "hobbies": Hobby.objects.all()

        }
        return render(request, "matches/complete_info.html", context)

    #friendslist.
    elif "action_friendslist" in request.POST:
        context = {
            "user": request.user,
            "friends": user.friendslist.all(),
            "sent_message": user.sent_message.all(),
            "received_message": user.received_message.all()
        }
        return render(request, "matches/friendslist.html", context)

    #match friends.
    elif "action_find_friends" in request.POST:
        hobbies = user.hobbies.all()
        age = user.age
        location = user.location.name
        #return a eductaion object.
        school = user.education
        nationality = user.nationality.name
        #return users.
        #exclude the current user.
        members = User_info.objects.exclude(username=request.user.username)
        existing_friends = user.friendslist.all()
        #exclude current friends.
        if existing_friends:
            for friend in existing_friends:
                members = [person for person in members if person.username != friend.username]

        # if user gave hobbies info, try match with hobbies first.
        if hobbies:
            #create a matching username list, set it to empty first.
            members_username = []
            for hobby in hobbies:
                #get a group of people for each hobby the user has.
                people = hobby.members.all()
                for person in people:
                    #if that username has not appeared before (since people might have more than one hobby), add it to the list.
                    if person.username not in members_username:
                        members_username.append(person.username)
            members = [person for person in members if person.username in members_username]
        #if user also gave ago info, try filter results with age range of +- 3.
        if age:
            members = [person for person in members if person.age in range(age-3, age+3)]
        #if user also gave location, try filter results with location.
        if location:
            members = [person for person in members if person.location.name == location]
        #if user also gave school, try filter results with school.
        if school:
            members = [person for person in members if person.education.name == school.name]
        #if user also gave nationality, try filter results with nationality.
        if nationality:
            members = [person for person in members if person.nationality.name == nationality]
        if not (hobbies or age or location or school or nationality):
            context = {
                "user": request.user,
                "message": "You need to give us more info about you !"

            }
            return render(request, "matches/user.html", context)

        context = {
            "user": request.user,
            "matches": members
        }
        return render(request, "matches/find_friends.html", context)

    #friendrequests.
    elif "action_friendrequests" in request.POST:
        friend_requests = user.receive.all()
        context = {
            "user": request.user,
            "requests": friend_requests
        }
        return render(request, "matches/friendrequests.html", context)


    #upload profile picture.
    elif "action_upload_profile_pic" in request.POST:
        context = {
            "user": user
        }
        return render(request, "matches/profile_pic.html", context)


    #logout.
    elif "action_logout" in request.POST:
        logout(request)
        return render(request, "matches/login.html", {"message": "Logged out."})


#complete info.
def complete_info_view(request):
    user = User_info.objects.get(username=request.user.username)
    hobbies = Hobby.objects.all()
    if "age" in request.POST:
        user.age = request.POST["age"]
        user.save()
    if "gender" in request.POST:
        user.gender = request.POST["gender"]
        user.save()
    if "nationality" in request.POST:
        user.nationality = request.POST["nationality"]
        user.save()
    if "location" in request.POST:
        user.location = request.POST["location"]
        user.save()
    if "education" in request.POST:
        education = Education.objects.get(name=request.POST["education"])
        user.education = education
        user.save()
    for hobby in hobbies:
        if hobby.name in request.POST:
            user.hobbies.add(hobby)
        user.save()

    context = {
        "user": request.user,
        "message": "Thank you for providing information about yourself! We will help you find more friends!"

    }
    return render(request, "matches/user.html", context)


#show users info.
def user_info_view(request, id):
    user = User_info.objects.get(id=id)
    you = User_info.objects.get(username=request.user.username)
    if user.friendslist and you.friendslist:
        sharedfriends_list = []
        for person in user.friendslist.all():
            for friend in you.friendslist.all():
                if friend.id == person.id:
                    sharedfriends_list.append(friend)
                    break
    context = {
        "user": user,
        "sharedfriends": sharedfriends_list
    }
    return render(request, "matches/user_info.html", context)

#send friend request.
def friend_request_view(request):
    to_user = User_info.objects.get(id=request.POST["user_id"])
    text = request.POST["message"]
    from_user = User_info.objects.get(username=request.user.username)
    friend_request = Friend_request(from_user=from_user, text=text, to_user=to_user)
    friend_request.save()
    context = {
        "user": request.user,
        "message": "friend request has been send!"

    }
    return render(request, "matches/user.html", context)

#manage friend request.
def process_request_view(request):
    user = User_info.objects.get(username=request.user.username)
    friend_requests = user.receive.all()
    if "action_accept" in request.POST:
        for r in friend_requests:
            if r.from_user.username in request.POST:
                from_u = User_info.objects.get(id=r.from_user.id)
                to_u = User_info.objects.get(id=r.to_user.id)
                from_u.friendslist.add(to_u)
                r.delete()
    elif "action_decline" in request.POST:
        for r in friend_requests:
            if r.from_user.username in request.POST:
                r.delete()

    message=""
    if "action_accept" in request.POST:
        message="Friend requests accepted."
    elif "action_decline" in request.POST:
        message="Friend requests declined."
    context = {
        "user": request.user,
        "message": message
    }
    return render(request, "matches/user.html", context)

def delete_friend_view(request):
    user = User_info.objects.get(username=request.user.username)
    friends = user.friendslist.all()
    for friend in friends:
        if friend.username in request.POST:
            remove_friend = User_info.objects.get(username=friend.username)
            user.friendslist.remove(remove_friend)

    context = {
        "user": request.user,
        "message": "You have removed a friend."
    }
    return render(request, "matches/user.html", context)

def message_view(request):
    users = User_info.objects.all()
    for user in users:
        if user.username in request.POST:
            from_user = User_info.objects.get(username=request.user.username)
            to_user = User_info.objects.get(username=user.username)
            text = request.POST["msg"]
            message = Message(from_user=from_user, text=text, to_user=to_user)
            message.save()
    context = {
        "user": request.user,
        "message": "Message sent."
    }
    return render(request, "matches/user.html", context)

def upload_pic_view(request):
    user = User_info.objects.get(username=request.user.username)
    if request.method == "POST" and request.FILES:
        mypic = request.FILES["img"]
    else:
        context = {
            "user": request.user,
            "message": "You need to select an image!"
        }
        return render(request, "matches/user.html", context)

    #if user has an old profile_pic in the system, delete it.
    if user.photo:
        os.remove(user.photo.path)
    user.photo = mypic
    user.save()
    #rename the picture to user's username so the name of picture is unique.
    inital_path = user.photo.path
    user.photo.name = f"users/{user.username}.jpg"
    new_path = settings.MEDIA_ROOT + user.photo.name
    os.rename(inital_path, new_path)
    user.save()
    context = {
        "user": request.user,
        "message": "Profile Picture Uploaded."
    }
    return render(request, "matches/user.html", context)
