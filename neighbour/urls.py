from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[
    url('^$',views.index,name='index'),
    url(r'^new/neighbourhood$', views.new_project, name='new-project'),
    url(r'^search/', views.search_projects, name='search'),
    url(r'^neighbourhoods/(\d+)',views.image,name ='image'),
    url(r'^ajax/newsletter/$', views.newsletter, name='newsletter'),
    url(r'^api/neighbourhoods/$', views.Projects.as_view()),

    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)