from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms


# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            print(username)
            print(password)


            try:
                user = models.WebUser.objects.get(username=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            if user.upwd == password:
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
    pass
    return redirect("/login/")
