from django.conf.urls import include, url
from django.contrib import  admin
from rest_framework import routers
from restaurant import views


urlpatterns = [
  url(r'^api/menus', views.MenuViewSet),
    url(r'^api/orders/', views.OrderViewSet),
    url(r'^api/info/', views.InfoViewSet),
    url(r'^api/rating/', views.RaitingViewSet),
    url(r'^admin/', admin.site.urls),
    url(r'^restaurant/', include('restaurant.urls', namespace='restaurant')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
