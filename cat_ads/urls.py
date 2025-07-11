from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),  # Включаем URL-маршруты из приложения 'ads'
    path('accounts/', include('django.contrib.auth.urls')), # Для login/logout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
