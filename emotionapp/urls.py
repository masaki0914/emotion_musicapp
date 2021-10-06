from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.image_upload,name='imageupload'),
    path('login/', views.Login.as_view(),name='login'),
    path('logout/', views.Logout.as_view(),name='logout'),
    path('signup/', views.signup, name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)