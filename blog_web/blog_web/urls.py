from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from blog.views import home, individual_blog, search, register, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('category/', include('blog.urls')),
    path('blogs/<slug:slug>/', individual_blog, name='individual_blog'),
    path('blog/search/', search, name='search'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', include('dashboard.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)