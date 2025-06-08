from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def test_view(request):
    return HttpResponse("No Hack")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", test_view),
    path('bot/', include('bot.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
