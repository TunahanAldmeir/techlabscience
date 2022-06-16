from django import template
from posts.models import category,tag,Post
from users.models import UserProfile

register=template.Library()

@register.simple_tag(name="categories")

def all_categories():
    return category.objects.all()

@register.simple_tag(name="tags")

def all_tags():
    return tag.objects.all()

@register.simple_tag(name='hit_posts')
def hit_posts():
    return Post.objects.order_by('-hit')[:5]

@register.simple_tag(name='images')
def gmen():
    return UserProfile.objects.all()
