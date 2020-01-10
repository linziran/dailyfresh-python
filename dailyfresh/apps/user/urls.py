
from user.views import LoginView,UserInfoView,UserOrderView,AddressView,LogoutView
from django.urls import path
from django.conf.urls import url
from user import views



urlpatterns = [
    path('register/',views.register,name='register'),#注册
    path('login/',LoginView.as_view(),name='login'),#登陆
    path('logout/',LogoutView.as_view(),name='logout'),#退出
    path('',UserInfoView.as_view(),name='user'),#用户中心-信息页
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    path('address/',AddressView.as_view(),name='address'),#用户中心-地址

]
