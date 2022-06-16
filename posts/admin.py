from django.contrib import admin

# Register your models here.
from posts.models import Post,category,tag,Comment


class AdminPost(admin.ModelAdmin):
    list_filter = ['publishing_date']
    list_display = ['title','publishing_date']
    search_fields =['title','content']

    class Meta:
        model=Post

class Admincomment(admin.ModelAdmin):
    list_filter = ("publishing_date",)
    search_fields = ('name','email','content','post__title')

    class Meta:
        model=Comment

admin.site.register(Post,AdminPost)
admin.site.register(category)
admin.site.register(tag)
admin.site.register(Comment,Admincomment)
