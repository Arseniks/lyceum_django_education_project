from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('', include('homepage.urls')),
    path('about/', include('about.urls')),
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('feedback/', include('feedback.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static('static_dev', document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
