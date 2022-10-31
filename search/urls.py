from django.urls import path
from .views import home, search_view, cooler_verification, cooler_verification_blank

urlpatterns = [
    path('', home),
    path('ici/', search_view, name = 'ici'),
    path('cvm/', cooler_verification_blank, name = 'cvm'),
    path('cvm/<int:time_jump>/<str:center>', cooler_verification)
]