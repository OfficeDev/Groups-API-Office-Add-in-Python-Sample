"""
Definition of urls for DjangoMyGroups.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
from app import views 

urlpatterns = patterns('', 
  # The home view ('/') 
  url(r'^$', views.home, name='home'),

  # Explicit home ('/login/') 
  url(r'^login/$', views.login, name='login'),
  # Groups view ('/groups/') 
  url(r'^groups/$', views.groups, name='groups'),
  # The group detail view ('/groups/123/') 
  url(r'^groups/(?P<group_id>[a-zA-Z0-9\-]+)/$', views.detail, name='detail'), 

  # Explicit home ('/addin/login/') 
  url(r'^addin/login/$', views.addinlogin, name='addinlogin'),
  # Groups view for add-ins ('/addin/groups/') 
  url(r'^addin/groups/$', views.addingroups, name='addingroups'),
  # The group detail view for add-in ('/addin/groups/123/') 
  url(r'^addin/groups/(?P<group_id>[a-zA-Z0-9\-]+)/$', views.addindetail, name='addindetail'), 
)