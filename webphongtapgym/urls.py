
from django import views
from django.contrib import admin
from django.urls import path, include
from Gym.consumers import NotificationConsumer
from Gym.views import home
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path('', home, name="home"),
    path('', include('Gym.urls')),
    path('', include('Users.urls')),
    path('', include('Checkouts.urls')),
    path('', include('Carts.urls')),
    # path('api/', include('Users.urls')),
    # path('api/', include('Gym.urls')),
    path('api/', include('Courses.urls')),
]
websocket_urlpatterns = [
    path('ws/notification/', NotificationConsumer.as_asgi()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
