from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
import mimetypes

from about.views import show_about, show_mission

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', show_about),
    path('about/mission/', show_mission),
    path('product/', include(('product.urls', 'product'))),
]

if settings.DEBUG:
    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))] + static(settings.MEDIA_URL,
                                                                              document_root=settings.MEDIA_ROOT)
