from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
 
from .views import RecentBlogView

urlpatterns = [
    path('recent/', RecentBlogView.as_view(), name='recent_posts'),
]