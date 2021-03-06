from captcha.fields import CaptchaField
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')
