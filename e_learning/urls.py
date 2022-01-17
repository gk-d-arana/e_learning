from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("control_panel/", include('frontend.urls')),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('extras.urls')),
    path('', include('courses.urls')),
    path('', include('orders.urls')),
    path('', include('chat.urls')),

]


#twisted-iocpsupport==1.0.2