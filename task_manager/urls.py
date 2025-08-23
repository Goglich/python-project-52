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
from task_manager.users import views as userViews
from task_manager.statuses import views as statusViews
from task_manager.tasks import views as taskViews
from task_manager.labels import views as labelViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='main_page'),
    path('users/', userViews.IndexView.as_view(), name='users'),
    path(
        'users/create/', 
        userViews.RegistrationView.as_view(), 
        name='create_user'),
    path('login/', userViews.LoginUserView.as_view(), name='login'),
    path('logout/', userViews.LogoutUserView.as_view()),
    path(
        'users/<int:user_id>/update/',
        userViews.UserEditView.as_view(),
        name='edit_user'),
    path(
        'users/<int:user_id>/delete/',
        userViews.UserDeleteView.as_view(),
        name='delete_user'),
    path('statuses/', statusViews.StatusView.as_view(), name='statuses'),
    path('statuses/create/', statusViews.CreateStatusView.as_view()),
    path(
        'statuses/<int:status_id>/update/',
        statusViews.EditStatusView.as_view(),
        name='edit_status'),
    path(
        'statuses/<int:status_id>/delete/',
        statusViews.StatusDeleteView.as_view(),
        name='delete_status'),
    path('tasks/', taskViews.TaskView.as_view(), name='tasks'),
    path(
        'tasks/<int:task_id>/', 
        taskViews.ShowTaskView.as_view(), 
        name='task'),
    path(
        'tasks/create/', 
        taskViews.CreateTaskView.as_view(), 
        name='tasks_create'),
    path(
        'tasks/<int:task_id>/update/',
        taskViews.EditTaskView.as_view(),
        name='edit_task'),
    path(
        'tasks/<int:task_id>/delete/',
        taskViews.DeleteTaskView.as_view(),
        name='delete_task'
        ),
    path('labels/', labelViews.LabelsView.as_view(), name='labels'),
    path(
        'labels/create/', 
        labelViews.CreateLabelView.as_view(), 
        name='create_label'),
    path(
        'labels/<int:label_id>/update/',
        labelViews.EditLabelView.as_view(),
        name='edit_label'
        ),
    path(
        'labels/<int:label_id>/delete/',
        labelViews.DeleteLabelView.as_view(),
        name='delete_label'
        ),
]
