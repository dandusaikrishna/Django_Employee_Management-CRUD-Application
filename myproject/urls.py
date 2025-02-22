from django.contrib import admin
from django.urls import path, include
from myapp.views import HomeView  # Import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),  
    path('', include('myapp.urls')),
]
