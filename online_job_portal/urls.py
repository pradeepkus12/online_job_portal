"""
URL configuration for online_job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django import views
from django.contrib import admin
from job import views
from django.urls import path
from job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name="index"),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_home', admin_home, name='admin_home'),
    path('admin_signup', admin_signup, name='admin_signup'), 
    path('user_login', user_login, name='user_login'),
    path('recruiter_login', recruiter_login, name='recruiter_login'),
    path('user_signup', user_signup, name='user_signup'), 
    path('user_home', user_home, name='user_home'),
    path('Logout', Logout, name='Logout'),
    path('recruiter_signup', recruiter_signup, name='recruiter_signup'),
    path('recruiter_home', recruiter_home, name='recruiter_home'),
    path('view_user', view_user, name='view_user'),
    path('recruiter_pending', recruiter_pending, name='recruiter_pending'),
    path('change_status/<int:recruiter_id>/', change_status, name='change_status'),
    path('recruiter_accepted', recruiter_accepted,name='recruiter_accepted'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('recruiter_rejected', recruiter_rejected, name='recruiter_rejected'),
    path('all_recruiters', all_recruiters, name='all_recruiters'),
    path('change_passwordadmin/',views.change_passwordadmin,name='change_passwordadmin'),
    path('change-passworduser/',views.change_passworduser,name='change_passworduser'),
    path('change-passwordrecruiter/',views.change_passwordrecruiter,name='change_passwordrecruiter'),
    path('add_job/',add_job, name='add_job'),
    path('job_list/', job_list, name='job_list'),
    path('latest_jobs/', latest_jobs, name='latest_jobs'),
    path('user_latestjobs/', user_latestjobs, name='user_latestjobs'),
    path('edit_jobdetail/<int:id>/', edit_jobdetail, name='edit_jobdetail'),
    path('delete_job/<int:id>/', delete_job, name='delete_job'),
    path('applyforjob/<int:id>/',views.applyforjob,name='applyforjob'),
    path('upload_resume/<int:id>/',views.upload_resume,name='upload_resume'),
    path('delete_recruiter/<int:recruiter_id>/', delete_recruiter, name='delete_recruiter'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
