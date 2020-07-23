from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from celery_tasks.tasks import send_register_active_email
from utils.mixin import LoginRequiredMixin
from itsdangerous import SignatureExpired
from user.models import User, Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
import re

# Create your views here.


def register(request):
    """显示注册页面"""
    if request.method == "GET":
        return render(request, "register.html")
    else:
        """进行注册处理"""
        # 接受数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        # print(username, password, email, allow)

        # # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, "register.html", {"errmsg": "数据不完整"})
        # 校验邮箱
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"errmsg": "邮箱不正确"})

        if allow != "on":
            return render(request, "register.html", {"errmsg": "请同意协议"})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            return render(request, "register.html", {"errmsg": "用户名已存在"})
        # 业务处理：用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答
        return redirect(reverse("goods:index"))


# /user/register
class RegisterView(View):
    def get(self, request):
        """显示注册页面"""
        return render(request, "register.html")

    def post(self, request):
        """进行注册处理"""
        # 接受数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        # print(username, password, email, allow)

        # # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, "register.html", {"errmsg": "数据不完整"})
        # 校验邮箱
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"errmsg": "邮箱不正确"})

        if allow != "on":
            return render(request, "register.html", {"errmsg": "请同意协议"})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            return render(request, "register.html", {"errmsg": "用户名已存在"})
        # 业务处理：用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接： http://127.0.0.1:8000/user/active/3
        # 激活的链接中需要包含用户的身份信息，并且把身份信息进行加密

        # 加密用户的身份信息，生成激活的token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 发邮件
        send_register_active_email.delay(email, username, token)
        # 授权码 啊= leuaojnnlqlrbfjc

        # 返回应答
        return redirect(reverse("goods:index"))


# /user/active/xxxx
class ActiveView(View):
    def get(self,  request, token):
        """进行用户激活"""
        # 获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取激活用户的id
            user_info = info["confirm"]

            # 根据id获取用户信息
            user = User.objects.get(id=user_info)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse("user:login"))
        except SignatureExpired:
            # 激活链接已过期
            return HttpResponse("激活链接已过期")


# /user/login
class LoginView(View):
    """登录"""
    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        return render(request, "login.html", {"username": username, "checked": checked})

    def post(self, request):
        # 接受数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        # 校验数据
        if not all([username, password]):
            return render(request, "login.html", {"errmsg": "数据不完整"})

        # 业务处理：登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户登录状态
                login(request, user)

                # 获取登录后所要跳转的地址
                next_url = request.GET.get("next", reverse("goods:index"))  # None

                # 跳转next_url
                response = redirect(next_url)

                # 判断是否记住用户名
                remember = request.POST.get("remember")
                if remember == "on":
                    response.set_cookie("username", username, max_age=24*3600)
                else:
                    response.delete_cookie("username")

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, "login.html", {"errmsg": "用户未激活"})
        else:
            # 账号密码错误
            return render(request, "login.html", {"errmsg": "用户名或密码错误"})


# /user/logout
class LogoutView(View):
    """退出登录"""
    def get(self, request):
        # 清除用户session信息
        logout(request)
        return redirect(reverse("goods:index"))


# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        """显示"""
        # page = 'user'
        user = request.user
        address = Address.object.get_default_address(user)

        # 获取用户的历史浏览记录

        con = get_redis_connection("default")  # 连接到redis数据库

        history_key = "history_%d" % user.id

        # 获取用户最新浏览的5个商品的id
        sku_id = con.lrange(history_key, 0, 4)

        # 遍历获取用户浏览的商品信息
        goods_li = []
        for id in sku_id:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        return render(request, "user_center_info.html", {"address": address, "goods_li": goods_li})


# /user/order
class UserOrderView(LoginRequiredMixin, View):
    def get(self, request, page):
        """显示"""
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by("-create_time")

        # 遍历获取订单商品信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性,保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性,保存订单商品的信息
            order.order_skus = order_skus
        # 分页
        paginator = Paginator(orders, 1)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        # todo: 进行页码的控制，页面上最多显示5个页码
        order_page = paginator.page(page)
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {
            "order_page": order_page,
            "pages": pages,
            "page": "order"
        }

        # 使用模板
        return render(request, "user_center_order.html", context)


# /user/address
class AddressView(LoginRequiredMixin, View):
    """用户中心-地址页"""
    def get(self, request):
        """显示"""
        # page = 'address'
        # 获取登录用户对用User对象
        user = request.user

        # 获取用户的默认收货地址
        address = Address.object.get_default_address(user)

        return render(request, "user_center_site.html", {"address": address})

    def post(self, request):
        """地址的添加"""
        receiver = request.POST.get("receiver")
        addr = request.POST.get("addr")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")

        if not all([receiver, addr, zip_code, phone]):
            return render(request, "user_center_site.html", {"errmsg": "数据不完整"})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, "user_center_site.html", {"errmsg": "手机格式不对"})

        # 业务处理
        # 如果用户已存在默认的收货地址，添加的地址不作为默认收货地址，否则做为默认收货地址
        # 获取登录用户User对象
        user = request.user

        address = Address.object.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.object.create(user=user, receiver=receiver, addr=addr,
                              zip_code=zip_code, phone=phone, is_default=is_default)

        # 返回应答，刷新地址页面
        return redirect(reverse("user:address"))





