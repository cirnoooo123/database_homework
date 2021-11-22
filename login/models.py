from django.db import models


# Create your models here.

# class User(models.Model):
#
#     gender = (
#         ('male', "男"),
#         ('female', "女"),
#     )
#
#     name = models.CharField(max_length=128, unique=True)
#     password = models.CharField(max_length=256)
#     email = models.EmailField(unique=True)
#     sex = models.CharField(max_length=32, choices=gender, default="男")
#     c_time = models.DateTimeField(auto_now_add=True)

class WebUser(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    upwd = models.CharField(max_length=18)
    loveMovies = models.ManyToManyField("Movie")
    loveDirectors = models.ManyToManyField("Director")
    loveActors = models.ManyToManyField("Actor")


class Movie(models.Model):
    style = (('0', "喜剧"), ('1', "悲剧"))

    movieName = models.CharField(max_length=100)
    movieIntroduction = models.CharField(max_length=500)
    movieDate = models.DateField()
    movieStyle = models.CharField(max_length=20, choices=style)
    moviePhoto = models.CharField(max_length=100)
    movieWard = models.CharField(max_length=30)
    movieCost = models.BigIntegerField()
    movieCompany = models.ForeignKey("Company", on_delete=models.CASCADE, null=True)


class Director(models.Model):
    directorName = models.CharField(max_length=30)
    directorAge = models.IntegerField()
    directorBir = models.CharField(max_length=30)
    directorPhoto = models.CharField(max_length=100)
    representativeMovies = models.ManyToManyField("Movie")


class Actor(models.Model):
    actorName = models.CharField(max_length=30)
    actorAge = models.IntegerField()
    actorBir = models.CharField(max_length=30)
    actorPhoto = models.CharField(max_length=100)
    majorActedMovies = models.ManyToManyField("Movie")


class Company(models.Model):
    companyName = models.CharField(max_length=30)
    companyAddr = models.CharField(max_length=30)


class Review(models.Model):
    reviewGrade = models.IntegerField()
    reviewString = models.CharField(max_length=200)
    reviewDate = models.DateField(auto_now=True)
    reviewedAuthor = models.ForeignKey("WebUser", on_delete=models.CASCADE, null=True)
    reviewedMovie = models.ForeignKey("Movie", on_delete=models.CASCADE, null=True)

