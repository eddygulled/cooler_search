from django.urls import path
from .views import search_view,record_data

urlpatterns = [
    path('', search_view),
    path("<str:tag>/<str:long>/<str:lat>", record_data, name="record_data")
]