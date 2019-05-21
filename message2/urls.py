from django.conf.urls import url
from django.contrib import admin
from message2 import views #导入 sign 应用 views 文件
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.index), #添加index/路径配置
]