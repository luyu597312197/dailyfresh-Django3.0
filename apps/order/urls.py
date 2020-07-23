from django.contrib import admin
from django.urls import path, include
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, CommentView

urlpatterns = [
    path("place_order", OrderPlaceView.as_view(), name="place"),  # 提交订单页面显示
    path("commit", OrderCommitView.as_view(), name="commit"),  # 订单创建
    path("pay", OrderPayView.as_view(), name="pay"),  # 订单支付
    path("check", CheckPayView.as_view(), name="check"),  # 查询支付交易结果
    path("check/<int:order_id>", CheckPayView.as_view(), name="check"),  # 查询支付交易结果【测试】
    path("comment/<int:order_id>", CommentView.as_view(), name="comment"),  # 查询支付交易结果
]
