from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms


# Create your views here.
def queryset2list(queryset):
    data = [entry for entry in queryset]
    return data


def login(request):
    if request.method == 'POST':
        if request.session.get('isLogin', None):
            return redirect('/index/')
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
            if user.upwd == password:
                request.session['isLogin'] = True
                request.session['userName'] = username
                return redirect('/index/')
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
                user = models.WebUser(username=username, upwd=password1)
                user.save()
                message = '注册成功！'
                return render(request, 'login/login.html', locals())
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('isLogin', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def index(request):
    user = models.WebUser.objects.get(username=request.session.get("userName"))
    result = {}
    movies = user.loveMovies.all().values()
    actors = user.loveActors.all().values()
    directors = user.loveDirectors.all().values()
    result["loveMovies"] = movies
    result["loveActors"] = actors
    result["loveDirectors"] = directors
    return render(request, 'login/index.html', result)


def movieList(request):
    if request.method == 'POST':
        movieName = request.POST.get("movieName")
        movies = models.Movie.objects.filter(movieName__contains=movieName).values()
        return render(request, 'login/movieList.html', {"result": movies})
    movies = models.Movie.objects.all().values()
    return render(request, 'login/movieList.html', {"result": movies})


def movie(request):
    if request.GET.get("type") == "loveMovie":
        userName = request.session.get("userName")
        movieId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        movieAdding = models.Movie.objects.get(id=movieId)
        user.loveMovies.add(movieAdding)
        return redirect("/movie?id=" + request.GET.get("id"))
    movieId = request.GET.get("id")
    m = models.Movie.objects.get(id=movieId)
    return render(request, 'login/movie.html', {"result": m})


def actorList(request):
    if request.method == 'POST':
        actorName = request.POST.get("actorName")
        actors = models.Actor.objects.filter(actorName__contains=actorName).values()
        return render(request, 'login/actorList.html', {"result": actors})
    actors = models.Actor.objects.all().values()
    for var in actors:
        print(var)
    return render(request, 'login/actorList.html', {"result": actors})


def actor(request):
    if request.GET.get("type") == "loveActor":
        userName = request.session.get("userName")
        actorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        actorAdding = models.Actor.objects.get(id=actorId)
        user.loveActors.add(actorAdding)
        return redirect("/actor?id=" + request.GET.get("id"))
    actorId = request.GET.get("id")
    m = models.Actor.objects.get(id=actorId)
    return render(request, 'login/actor.html', {"result": m})


def directorList(request):
    if request.method == 'POST':
        directorName = request.POST.get("directorName")
        directors = models.Director.objects.filter(directorName__contains=directorName).values()
        return render(request, 'login/directorList.html', {"result": directors})
    directors = models.Director.objects.all().values()
    return render(request, 'login/directorList.html', {"result": directors})


def director(request):
    if request.GET.get("type") == "loveDirector":
        userName = request.session.get("userName")
        directorId = request.GET.get("id")
        user = models.WebUser.objects.get(username=userName)
        directorAdding = models.Director.objects.get(id=directorId)
        user.loveDirectors.add(directorAdding)
        return redirect("/director?id=" + request.GET.get("id"))
    directorId = request.GET.get("id")
    m = models.Director.objects.get(id=directorId)
    return render(request, 'login/director.html', {"result": m})


def companyList(request):
    if request.method == 'POST':
        companyName = request.POST.get("companyName")
        companys = models.Company.objects.filter(companyName__contains=companyName).values()
        return render(request, 'login/companyList.html', {"result": companys})
    companys = models.Company.objects.all().values()
    return render(request, 'login/companyList.html', {"result": companys})


def company(request):
    companyId = request.GET.get("id")
    m = models.Company.objects.get(id=companyId)
    return render(request, 'login/company.html', {"result": m})
