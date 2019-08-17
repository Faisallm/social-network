from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_view
from django.urls import path

app_name = 'account'

urlpatterns = [
    #url(r'^login/$', views.user_login, name='login'),
    url(r'^login/$', auth_view.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_view.LogoutView.as_view(), name='logout'),    
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password_change/$', auth_view.PasswordChangeView.as_view(), 
    {'post_change_redirect' : 'account:password_change_done'}, name='password_change'),
    url(r'^password_change/done/$', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password-reset/$', auth_view.PasswordResetView.as_view(), {'post_reset_redirect':'account:password_reset_done'}, name='password_reset'),
    url(r'^password-reset/done/$', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_view.PasswordResetConfirmView.as_view(), {'post_reset_redirect':'account:password_reset_complete'} ,name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
    
]