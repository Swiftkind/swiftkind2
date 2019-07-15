from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def avatar_url(user, size=50):
    """
    A template tag that receives a user and size and return
    the appropiate avatar url for that user.
    Example usage: {% avatar_url request.user 50 %}
    """
    if hasattr(user, 'avatar') and user.avatar:
        return user.avatar.url
    return static('wagtailadmin/images/default-user-avatar.png')