from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def mediapath(value):
    if value:
        return f"/media/{value}"
    else:
        return '/media/subs/dinn_logo_white.png'
        # return '/media/catalog/dinn_logo_white.png'

@register.filter()
def is_moderator(user):
    return user.groups.filter(name='moderator').exists()

# def is_superuser(user):
#     return user.is_superuser
