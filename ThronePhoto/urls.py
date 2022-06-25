from django.contrib import admin
from django.urls import path
from main.views import login_view, index, logout_view
from main.model_view import PhotographyListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', PhotographyListView.as_view(), name='home'),
                  path('accounts/login/', login_view, name='login-view'),
                  path('accounts/logout/', logout_view, name='logout-view')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
