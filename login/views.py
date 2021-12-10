import random

from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def queryset2list(queryset):
    data = [entry for entry in queryset]
    return data


def login(request):
    if request.method == 'POST':
        if request.session.get('isLogin', None):
            return redirect('/login/')
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.WebUser.objects.get(username=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            if check_password(password,user.upwd):
                request.session['isLogin'] = True
                request.session['userName'] = username
                return redirect('/login/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        try:
            user = models.WebUser.objects.get(username=username)
            print(user.username)
            message = '用户已经存在！'
            return render(request, 'login/register.html', locals())
        except:
            if password1 != password2:
                message = '密码输入不一致！'
                return render(request, 'login/register.html', locals())
            else:
                user = models.WebUser(username=username, upwd=make_password(password1))
                print(make_password(password1))
                user.save()
                message = '注册成功！'
                return redirect("/login/login/")
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('isLogin', None):
        return redirect("/login/login")
    request.session.flush()
    return redirect("/login/login")


def recMovie(name):
    movies = []
    style = {}
    for var in models.WebUser.objects.get(username=name).loveMovies.all():
        if var.movieStyle in style.keys():
            style[var.movieStyle] = style[var.movieStyle] + 1
        else:
            style[var.movieStyle] = 1
    if len(style) == 0:
        last = models.Movie.objects.count() - 1
        for i in range(5):
            index1 = random.randint(0, last)
            movies.append(models.Movie.objects.all()[index1])
        return movies
    elif len(style) == 1:
        for var in style.keys():
            movies1 = models.Movie.objects.filter(movieStyle__contains=var)
            last = movies1.count() - 1
            for i in range(3):
                index1 = random.randint(0, last)
                movies.append(movies1[index1])
        last = models.Movie.objects.count() - 1
        for i in range(2):
            index1 = random.randint(0, last)
            movies.append(models.Movie.objects.all()[index1])
        return movies
    else:
        first = 0
        firstStyle = None
        for var in style.keys():
            if style[var] > first:
                first = style[var]
                firstStyle = var

        second = 0
        secondStyle = None
        for var in style.keys():
            if style[var] > second and var != firstStyle:
                second = style[var]
                secondStyle = var
        movies1 = models.Movie.objects.filter(movieStyle__contains=firstStyle)
        last = movies1.count() - 1
        for i in range(3):
            index1 = random.randint(0, last)
            movies.append(movies1[index1])
        movies1 = models.Movie.objects.filter(movieStyle__contains=secondStyle)
        last = movies1.count() - 1
        for i in range(2):
            index1 = random.randint(0, last)
            movies.append(movies1[index1])
        return movies


def index(request):

    if request.session.get("userName") is None:
        return redirect("/login/login/")
    result = {}

    movies2 = recMovie(request.session['userName'])


    actors2 = []
    last = models.Actor.objects.count() - 1
    for i in range(5):
        index = random.randint(0, last)
        actors2.append(models.Actor.objects.all()[index])

    last = models.Director.objects.count() - 1
    directors2 = []
    for i in range(5):
        index = random.randint(0, last)
        directors2.append(models.Director.objects.all()[index])

    result["recMovies"] = movies2
    result["recActors"] = actors2
    result["recDirectors"] = directors2
    return render(request, 'login/index.html', result)


def movieList(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    styleSet = set()
    movies = models.Movie.objects.all().values()
    for var in movies:
        s = var.get("movieStyle").split(" ")
        for style in s:
            styleSet.add(style)

    if request.method == 'POST':
        movieName = request.POST.get("movieName")
        movies = models.Movie.objects.filter(movieName__contains=movieName).values()
        return render(request, 'login/movieList.html', {"result": movies, "styles": styleSet})

    if request.GET.get("type") == "queryStyle":
        movies = models.Movie.objects.filter(movieStyle__contains=request.GET.get("style"))
        return render(request, 'login/movieList.html', {"result": movies, "styles": styleSet})

    if request.GET.get("type") == "orderBy":
        movies = models.Movie.objects.all().order_by("-movieDate").values()
        return render(request, 'login/movieList.html', {"result": movies, "styles": styleSet})
    return render(request, 'login/movieList.html', {"result": movies, "styles": styleSet})


def movie(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    message = ""
    if request.GET.get("type") == "loveMovie":
        userName = request.session.get("userName")
        movieId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        movieAdding = models.Movie.objects.get(id=movieId)
        user.loveMovies.add(movieAdding)
        return redirect("/login/movie?id=" + request.GET.get("id"))

    elif request.GET.get("type") == "deLoveMovie":
        userName = request.session.get("userName")
        movieId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        movieAdding = models.Movie.objects.get(id=movieId)
        user.loveMovies.remove(movieAdding)
        return redirect("/login/movie?id=" + request.GET.get("id"))

    elif request.method == 'POST':
        if not str.isdigit(request.POST.get("reviewGrade")) or not 1 <= int(request.POST.get("reviewGrade")) <= 5:
            message = "评分为1-5的数字，请检查输入"
        elif len(request.POST.get("reviewString")) > 200:
            message = "评论过长"
        else:
            message = "评论成功"
            reviewGrade = int(request.POST.get("reviewGrade"))
            reviewString = request.POST.get("reviewString")
            movieId = request.GET.get("id")
            newReview = models.Review(reviewGrade=reviewGrade, reviewString=reviewString,
                                      reviewedAuthor_id=request.session.get("userName"), reviewedMovie_id=movieId)
            newReview.save()

    movieId = request.GET.get("id")
    m = models.Movie.objects.get(id=movieId)
    reviews = m.review_set.all().values()
    actors = m.actor_set.all().values()
    directors = m.director_set.all().values()
    return render(request, 'login/movie.html',
                  {"result": m, "reviews": reviews, "actors": actors, "directors": directors, "message": message})


def actorList(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.method == 'POST':
        actorName = request.POST.get("actorName")
        actors = models.Actor.objects.filter(actorName__contains=actorName).values()
        return render(request, 'login/actorList.html', {"result": actors})
    actors = models.Actor.objects.all().values()
    for var in actors:
        print(var)
    return render(request, 'login/actorList.html', {"result": actors})


def actor(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.GET.get("type") == "loveActor":
        userName = request.session.get("userName")
        actorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        actorAdding = models.Actor.objects.get(id=actorId)
        user.loveActors.add(actorAdding)
        return redirect("/login/actor?id=" + request.GET.get("id"))

    elif request.GET.get("type") == "deLoveActor":
        userName = request.session.get("userName")
        actorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        actorAdding = models.Actor.objects.get(id=actorId)
        user.loveActors.remove(actorAdding)
        return redirect("/login/actor?id=" + request.GET.get("id"))

    actorId = request.GET.get("id")
    m = models.Actor.objects.get(id=actorId)
    movies = m.majorActedMovies.all().values()
    return render(request, 'login/actor.html', {"result": m, "movies": movies})


def directorList(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.method == 'POST':
        directorName = request.POST.get("directorName")
        directors = models.Director.objects.filter(directorName__contains=directorName).values()
        return render(request, 'login/directorList.html', {"result": directors})
    directors = models.Director.objects.all().values()
    return render(request, 'login/directorList.html', {"result": directors})


def director(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.GET.get("type") == "loveDirector":
        userName = request.session.get("userName")
        directorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        directorAdding = models.Director.objects.get(id=directorId)
        user.loveDirectors.add(directorAdding)
        return redirect("/login/director?id=" + request.GET.get("id"))
    elif request.GET.get("type") == "deLoveDirector":
        userName = request.session.get("userName")
        directorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        directorAdding = models.Director.objects.get(id=directorId)
        user.loveDirectors.remove(directorAdding)
        return redirect("/login/director?id=" + request.GET.get("id"))

    directorId = request.GET.get("id")
    m = models.Director.objects.get(id=directorId)
    movies = m.representativeMovies.all().values()
    return render(request, 'login/director.html', {"result": m, "movies": movies})


def companyList(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.method == 'POST':
        companyName = request.POST.get("companyName")
        companys = models.Company.objects.filter(companyName__contains=companyName).values()
        return render(request, 'login/companyList.html', {"result": companys})
    companys = models.Company.objects.all().values()
    return render(request, 'login/companyList.html', {"result": companys})


def company(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    companyId = request.GET.get("id")
    m = models.Company.objects.get(id=companyId)
    movies = m.movie_set.all().values()
    return render(request, 'login/company.html', {"result": m, "movies": movies})


def userPage(request):
    if request.session.get("userName") is None:
        return redirect("/login/login/")
    if request.GET.get("type") == "deleteReview":
        deletingReview = models.Review.objects.get(id=request.GET.get("reviewId"))
        models.Review.delete(deletingReview)

    user = models.WebUser.objects.get(username=request.session.get("userName"))
    result = {}
    movies = user.loveMovies.all().values()
    actors = user.loveActors.all().values()
    directors = user.loveDirectors.all().values()
    reviews = user.review_set.all().values()

    result["loveMovies"] = movies
    result["loveActors"] = actors
    result["loveDirectors"] = directors
    result["reviews"] = reviews

    return render(request, 'login/userPage.html', result)
