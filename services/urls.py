from django.urls import path
from .views import index, ContentEmployeeView


urlpatterns = [
    path('', index, name='index'),
    path('content_employee/', ContentEmployeeView.as_view(), name='contentemployee')
]
