# news/urls.py
from django.urls import path, re_path
from . import views, admin_views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<int:pk>/', views.news_detail, name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/vote/(?P<value>-?\d+)/$', views.vote_news, name='vote'),

    path('export/', admin_views.export_xlsx_view, name='admin_export'),
]