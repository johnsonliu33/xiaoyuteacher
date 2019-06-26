from django.conf.urls import url
from django.contrib import admin
from message2 import views #导入 sign 应用 views 文件



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^index/$',views.index), #添加index/路径配置
    url(r'^login_action/', views.login_action),
    url(r'^device_manage/$', views.device_manage),
    url(r'^search_name/$', views.search_name),
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^logout/$', views.logout),
    url(r'^device_index/(?P<device_id>[0-9]+)/$', views.device_index),
    #url(r'^message_index_action/(?P<message_mid>[0-9]+)/$', views.message_index_action),
    url(r'^add_new_devices', views.add_device),
    url(r'^search_devices', views.get_device_content),
    url(r'^borrow_mobile', views.borrow_mobile),
    url(r'^repay_mobile', views.repay_mobile),

]