from django import template
from django.conf import settings

register = template.Library()


@register.filter()
def mediapath(value):
    if value:
        return f"/media/{value}"
    else:
        return '/media/dinn_logo_red.png'

@register.filter()
def is_moderator(user):
    return user.groups.filter(name='moderator').exists()

# def is_superuser(user):
#     return user.is_superuser

@register.filter()
def mediapathvideo(value):
    # return f"/media/{value}"
    if value:
        return f"/media/{value}"
    else:
        # return '/media/homer.mp4'
        return None
