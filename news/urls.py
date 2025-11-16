# news/urls.py
from django.urls import path, re_path
from . import views, admin_views
from django.contrib.auth import views as auth_views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<int:pk>/', views.news_detail, name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/vote/(?P<value>-?\d+)/$', views.vote_news, name='vote'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='news:list'), name='logout'),
    path('register/', views.register, name='register'),

    # Экспорт
    path('export/', admin_views.export_xlsx_view, name='admin_export'),
]