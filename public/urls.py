from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('maintenance/', TemplateView.as_view(template_name='public/maintenance.html'), name="maintenance"),
]