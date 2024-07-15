from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from django.contrib.auth.urls import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet/' , include("tweet.urls")) ,
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('index', views.fn, name = "basic"),

    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    