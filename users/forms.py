from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    username=forms.CharField()
    email=forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','password1','password2')

class UserProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,*kwargs)
        self.helper=FormHelper()
        self.helper.form_method="post"
        self.helper.field_class='mt-10'
        self.helper.layout=Layout(
            Field("birth_day",css_class="single-input"),
            Field("bio",css_class="single-input"),
            Field("image",css_class="single-input"),
        )
        self.helper.add_input(Submit('submit','Update',css_class="genric-btn succces-border medium"))


    class Meta:
        model=UserProfile
        fields=('birth_day','bio','image')
        widgets={
            'birth_day':forms.DateInput(attrs={"type":"date"})
        }
