from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^command$', views.command, name='Command'),
    url(r'^main$', views.index, name='Index'),
    url(r'^upload$', views.upload, name='Upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
