from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/a-silly-list-url/$', 'lists.views.view_list', 
        name='view_list'
    ),
)
