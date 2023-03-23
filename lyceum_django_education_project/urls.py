import ckeditor_uploader.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
from django.urls import include
from django.urls import path

import about.urls
import catalog.urls
import download.urls
import feedback.urls
import homepage.urls
import users.urls

urlpatterns = [
    path('', include(homepage.urls)),
    path('about/', include(about.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include(users.urls)),
    path('auth/', include(django.contrib.auth.urls)),
    path('catalog/', include(catalog.urls)),
    path('download/', include(download.urls)),
    path('feedback/', include(feedback.urls)),
    path('ckeditor/', include(ckeditor_uploader.urls)),
]

urlpatterns += static('static_dev', document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
