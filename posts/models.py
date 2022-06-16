from django.conf import settings
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify

class category(models.Model):
    title=models.CharField(max_length=250)
    slug=models.SlugField(editable=False)


    def __str__(self):
        return self.title


    def save1(self,*args,**kwargs,):
        self.slug=slugify(self.title)
        super(category,self).save(*args,**kwargs)

    def count(self):
        return self.posts.all().count()


class tag(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(editable=False)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(tag,self).save(*args,**kwargs)

    def post_count(self):
        return self.posts.all().count()









class Post(models.Model):
    title=models.CharField(max_length=150)
    content=models.TextField()
    publishing_date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(blank=True,null=True,upload_to="uploads/",default="uploads/blog-placeholder.jpg")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=1)

    slug=models.SlugField(default="slug",editable=False)

    category=models.ForeignKey(category,on_delete=models.CASCADE,default=1,related_name='posts')

    tag=models.ManyToManyField(tag,related_name='posts',blank=True)

    slider_posts=models.BooleanField(default=False)

    hit=models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)


    def post_tag(self):
        return ','.join(str(tag) for tag in self.tag.all())

    def comment_count(self):
        return self.comments.all().count()


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name=models.CharField(max_length=100)
    email=models.EmailField()
    content=models.TextField()
    publishing_date=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.post.title
