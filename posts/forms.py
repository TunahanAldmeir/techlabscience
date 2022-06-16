from captcha.fields import ReCaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,Submit

from .models import *
from django import forms

class PostCreationForm(forms.ModelForm):

    class Meta:
        model=Post
        widgets={
            'title':forms.TextInput(attrs={'class':'single-input','placeholder':'Yazı başlığı giriniz'}),
            'content':forms.Textarea(attrs={'class':'single-input','placeholder':'Yazı içeriği giriniz'}),
        }




        fields=[
            'title',
            'category',
            'content',
            'image'

        ]

class PostUpdateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PostUpdateForm,self).__init__(*args,**kwargs)
        self.helper=FormHelper()
        self.helper.form_method='post'
        self.helper.form_class='mt-10'
        self.helper.layout=Layout(
            Field("title",css_class="single-input",placeholder="Title"),
            Field("category",css_class="single-input",),
            Field("content",css_class="single-input",placeholder="İçerik Ekleyiniz"),
            Field("image",css_class="single-input"),
            Field("tag",css_class="single-input",placeholder="Etiketler",value=self.instance.post_tag()),
        )
        self.helper.add_input(Submit('submit',"Update Post",css_class="genric-btn success circle"))


    tag=forms.CharField()


    class Meta:
        model=Post
        fields=[
            'title',
            'category',
            'content',
            'image',
        ]

class CreateCommentfrom(forms.ModelForm):
    captcha=ReCaptchaField()

    def __init__(self,*args,**kwargs):
        super(CreateCommentfrom, self).__init__(*args,**kwargs)
        self.helper=FormHelper()
        self.helper.form_method='post'
        self.helper.layout=Layout(
            Field('name',css_class="form-control"),
            Field('email',css_class="form-control"),
            Field('content',css_class="from-control mb-10"),
            Field('captcha'),
        )

        self.helper.add_input(Submit("submit",'Yorum Ekle',css_class="primary-btn submit_btn"))


    class Meta:
        model=Comment
        fields=[
            'name',
            'email',
            'content',
        ]