from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='russian_pluralize')
def russian_pluralize(value, arg="комментарий,комментария,комментариев"):
    args = arg.split(",")
    if not value:
        return args[2]
    elif value % 10 == 1 and value % 100 != 11:
        return args[0]
    elif 2 <= value % 10 <= 4 and not (value % 100 >= 12 and value % 100 <= 14):
        return args[1]
    else:
        return args[2]
    
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''
    
@register.filter(name='has_liked')
def has_liked(comment, user):
    return comment.likes.filter(id=user.id).exists()

@register.filter(name='has_disliked')
def has_disliked(comment, user):
    return comment.dislikes.filter(id=user.id).exists()