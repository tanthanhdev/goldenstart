
from django.conf.urls import include
from django.urls import path
from sesame.views import LoginView


from . import views


urlpatterns = [
    path("sesame/login/", LoginView.as_view(), name="sesame-login"),
    path('', views.index, name="index"),
    path('retrieval-page', views.retrieval_page, name="retrieval-page"),
    
    # actions
    path('subscribe', views.subscribe, name='subscribe'),
    path('upload-file', views.upload_file, name='upload_file'),
    path('post-downloaded', views.post_downloaded, name='post_downloaded'),
    path('post-visited', views.post_visited, name='post_visited'),
    
]