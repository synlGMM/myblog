from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    """docstring for UserRegisterForm"""
    email = forms.EmailField(label='Email')
    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试。')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')