from django.conf.urls import url
from django.contrib import admin
from message2 import views #导入 sign 应用 views 文件



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^index/$',views.index), #添加index/路径配置
    url(r'^login_action/', views.login_action),
    url(r'^event_manage/$', views.event_manage),
    url(r'^accounts/login/$', views.login_action),
    url(r'^search_name/$', views.search_name),
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^logout/$', views.logout),
    url(r'^borrow_index/(?P<message_mid>[0-9]+)/$', views.message_index),
]