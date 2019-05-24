from django.conf.urls import url
from django.contrib import admin
from message2 import views #导入 sign 应用 views 文件



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^index/$',views.index), #添加index/路径配置
    url(r'^login_action/', views.login_action),
    url(r'^event_manage/$', views.event_manage),
    url(r'^accounts/login/$', views.login_action),
]