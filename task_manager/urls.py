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
from task_manager.users.views import IndexView, RegistrationView, LoginUserView, LogoutUserView, UserEditView, UserDeleteView
from task_manager.statuses.views import StatusView, CreateStatusView, EditStatusView, StatusDeleteView
from task_manager.tasks.views import TaskView, ShowTaskView, CreateTaskView, EditTaskView, DeleteTaskView
from task_manager.labels.views import LabelsView, CreateLabelView, EditLabelView, DeleteLabelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='main_page'),
    path('users/', IndexView.as_view(), name='users'),
    path('users/create/', RegistrationView.as_view(), name='create_user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view()),
    path('users/<int:user_id>/update/', UserEditView.as_view(), name='edit_user'),
    path('users/<int:user_id>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('statuses/', StatusView.as_view(), name='statuses'),
    path('statuses/create/', CreateStatusView.as_view()),
    path('statuses/<int:status_id>/update/', EditStatusView.as_view(), name='edit_status'),
    path('statuses/<int:status_id>/delete/', StatusDeleteView.as_view(), name='delete_status'),
    path('tasks/', TaskView.as_view(), name='tasks'),
    path('tasks/<int:task_id>/', ShowTaskView.as_view(), name='task'),
    path('tasks/create/', CreateTaskView.as_view(), name='tasks_create'),
    path('tasks/<int:task_id>/update/', EditTaskView.as_view(), name='edit_task'),
    path('tasks/<int:task_id>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('labels/', LabelsView.as_view(), name='labels'),
    path('labels/create/', CreateLabelView.as_view(), name='create_label'),
    path('labels/<int:label_id>/update/', EditLabelView.as_view(), name='edit_label'),
    path('labels/<int:label_id>/delete/', DeleteLabelView.as_view(), name='delete_label'),
]
