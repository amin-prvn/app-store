from django.contrib import admin
from django.conf import settings 
from django.urls import path, include
from django.conf.urls.static import static

# TODO Change with the app list page link
admin.site.site_url = 'Https://formaloo.com' 
admin.site.site_header = 'Formaloo App Store Admin'

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/v1/auth/', include('account.urls')),
    path('api/v1/', include('app.urls')),                            
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
