from django.db import models
from django_countries.fields import CountryField
# Create your models here.

class Hobby(models.Model):
    #sports.
    #art.
    #video games.
    #movies.
    #travel.
    #food.
    #music.

    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Education(models.Model):
    #elementary school.
    #middle school.
    #high school.
    #college.
    #graduate school.
    #phd.
    #home school.
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"







class User_info(models.Model):
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    age = models.IntegerField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    gender = models.CharField(max_length=64, blank=True)
    nationality = CountryField(blank=True, null=True)
    location = CountryField(blank=True, null=True)

    hobbies = models.ManyToManyField(Hobby, related_name="members", blank=True)

    education = models.ForeignKey(Education, related_name="members", on_delete=models.PROTECT, blank=True, null=True)

    friendslist = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Friend_request(models.Model):
    from_user = models.ForeignKey(User_info, related_name="send", on_delete=models.CASCADE)
    text = models.CharField(max_length=999, null=True)
    to_user = models.ForeignKey(User_info, related_name="receive", on_delete=models.CASCADE)

class Message(models.Model):
    from_user = models.ForeignKey(User_info, related_name="sent_message", on_delete=models.CASCADE)
    text = models.CharField(max_length=999, null=True)
    to_user = models.ForeignKey(User_info, related_name="received_message", on_delete=models.CASCADE)
