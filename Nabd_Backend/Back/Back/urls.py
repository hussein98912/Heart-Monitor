
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('doctor.urls')),
    path('api/', include('patient.urls')),
    path('api/', include('ai.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
