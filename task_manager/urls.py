"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import HomePageView
from User.views import IndexView, RegistrationView, LoginUserView, LogoutUserView, UserEditView, UserDeleteView
from status.views import StatusView, CreateStatusView, EditStatusView, StatusDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='main_page'),
    path('users/', IndexView.as_view(), name='users'),
    path('users/create/', RegistrationView.as_view()),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view()),
    path('users/<int:user_id>/update/', UserEditView.as_view(), name='edit_user'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('statuses/', StatusView.as_view(), name='statuses'),
    path('statuses/create/', CreateStatusView.as_view()),
    path('statuses/<int:status_id>/update/', EditStatusView.as_view(), name='edit_status'),
    path('statuses/<int:status_id>/delete/', StatusDeleteView.as_view(), name='delete_status'),
]
