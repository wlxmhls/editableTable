# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

from cmdb import index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_URL}),

    url(r'^$', index.table, name='home'),

    url(r'^tablenew$', index.tablenew),
    url(r'^tablenewform$', index.tablenewform),
    url(r'^tableclr$', index.tableclr),
    url(r'^tabledel$', index.tabledel),

    url(r'^cellupdate$', index.cellupdate),
    url(r'^celladd$', index.celladd),
    url(r'^celldel$', index.celldel),

    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register/', index.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
]
