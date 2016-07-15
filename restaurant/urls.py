from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^menus/$', views.index,name='index'),
    url(r'^orders/$', views.index_o,name='index_o'),

    url(r'^menus/(?P<menu_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^orders/(?P<order_id>[0-9]+)/$', views.detail_o, name='detail_o'),


    url(r'^today/$', views.index_t,name='index_t'),
    url(r'^menu/add/$', views.post_new, name='post_new'),
    url(r'^order/add/$', views.post_order	, name='post_order'),
    url(r'^change/(?P<order_id>[0-9]+)/$', views.change, name='change'),
]
		