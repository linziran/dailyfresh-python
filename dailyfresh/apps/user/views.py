from django.shortcuts import render,redirect,reverse
import re
from django.core.paginator import Paginator
from user.models import User,Address
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from utils.mixin import LoginRequiredMixin
from order.models import OrderInfo,OrderGoods
# Create your views here.
#注册
def register(request):
    '''注册'''
    if request.method =='GET':
        #'''显示注册页面'''
        return render(request,'register.html')
    else:
        #'''进行注册处理 '''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已经存在'})

        # 进行用户处理
        user = User.objects.create_user(username, email, password)

        # 返回应答,跳转到首页
        return redirect(reverse('goods:index'))

class LoginView(View):
    '''登陆'''
    def get(self, request):
        '''显示登陆页面'''
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        return render(request,'login.html',{'username':username,'checked':checked})
    def post(self,request):
        '''登陆校验'''
        #接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        #校验数据
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)

            #获取登陆后所要跳转的地址
            next_url=request.GET.get('next',reverse('goods:index'))
            #跳转到首页
            return redirect(next_url)
            # 判断是否需要记住用户名
            remember = request.POST.get('remember')

            if remember == 'on':
                #记住用户名
                response.set_cookie('username',username,max_age=7*24*3600)
            else:
                response.delete_cookie('username')
            return response
        else:
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})
        #登陆校验
        #返回应答

class LogoutView(View):
    '''退出登陆'''
    def get(self,request):
        logout(request)
        # 返回应答,跳转到首页
        return redirect(reverse('goods:index'))


#/user
class UserInfoView(LoginRequiredMixin,View):
    '''用户信息-信息页'''
    def get(self,request):
        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)
        return render(request,'user_center_info.html',{'page':'user','address':address})

# /user/order
class UserOrderView(LoginRequiredMixin, View):
    '''用户中心-订单页'''
    def get(self, request, page):
        '''显示'''
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count*order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性，保存订单商品的信息
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
        order_page = paginator.page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
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
        context = {'order_page':order_page,
                   'pages':pages,
                   'page': 'order'}

        # 使用模板
        return render(request, 'user_center_order.html', context)

#/user/address
class AddressView(LoginRequiredMixin,View):
    '''用户信息-地址页'''
    def get(self,request):
        '''显示'''
        # 获取登录用户对应User对象
        user = request.user

        # 获取用户的默认收货地址
        address = Address.objects.get_default_address(user)

        # 使用模板
        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self,request):
        '''地址的添加'''
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone, type]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})
         # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        address = Address.objects.get_default_address(user)
        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address')) # get请求方式