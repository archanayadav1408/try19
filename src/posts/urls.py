from django.conf.urls import url
from django.contrib import admin
from .views import (
	posts_create,
	posts_list,
	posts_delete,
	posts_detail,
	posts_update,
    )

urlpatterns = [
      url(r'^$', posts_list,name="list"),
      url(r'^create/$', posts_create),
      url(r'^(?P<slug>[\w-]+)/delete/$', posts_delete),
      url(r'^(?P<slug>[\w-]+)/$', posts_detail,name='detail'),
      url(r'^(?P<slug>[\w-]+)/edit/$', posts_update,name='update'),
     # url(r'^posts/', "<appname>.views.<function_name>"),

]
