from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # 기본 UserCreationForm 은 email 필드를 제공하지 않기 때문에
    # email 입력을 위한 form 을 상속하여 만든다.
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
