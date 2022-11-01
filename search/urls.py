from django.urls import path
from .views import home, search_view, cooler_verification,rad_cooler_verification, cooler_verification_blank, upload_file, error, login_view,activate_file

urlpatterns = [
    path('', home),
    path('activate/<int:file_id>/', activate_file, name='activate'),
    path('ici/', search_view, name='ici'),
    path('cvm/', cooler_verification_blank, name='cvm'),
    path('cvm/<int:time_jump>/<str:center>', cooler_verification),
    path('cvm/<str:center>/<int:time_jump>/', rad_cooler_verification),
    path('upload/', upload_file, name='upload'),
    path('error/', error, name='error'),
    path('login/', login_view, name='login'),
]
