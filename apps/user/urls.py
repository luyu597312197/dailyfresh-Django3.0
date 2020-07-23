from user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView, LogoutView
from django.urls import path

urlpatterns = [
    # path("register", views.register, name="register"),  # 注册
    # path("register_handle", views.register_handle, name="register_handle")  # 注册处理

    path("register", RegisterView.as_view(), name="register"),  # 注册
    path("active/<str:token>", ActiveView.as_view(), name="active"),  # 用户激活
    path("login", LoginView.as_view(), name="login"),  # 登录页面

    path("logout", LogoutView.as_view(), name="logout"),  # 退出登录

    # path("", login_required(UserInfoView.as_view()), name="user"),  # 用户中心-信息
    # path("order", login_required(UserOrderView.as_view()), name="order"),  # 用户中心-订单页
    # path("address", login_required(AddressView.as_view()), name="address"),  # 用户中心-地址页

    path("", UserInfoView.as_view(), name="user"),  # 用户中心-信息
    path("order/<int:page>", UserOrderView.as_view(), name="order"),  # 用户中心-订单页
    path("address", AddressView.as_view(), name="address"),  # 用户中心-地址页
]
