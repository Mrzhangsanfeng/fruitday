from django.shortcuts import render, redirect

from memberapp.models import Goods
from userinfo.models import UserInfo
from userinfo.models import Address

from .models import *
from django.http import HttpResponse
from django.db import DatabaseError
import logging
import json
import datetime


# Create your views here.

def add_cart(request):
    # 获取前端数据(商品id,商品数量,)
    # 获取用户id
    # 查数据库
    # 存
    # 返回页面

    # user_id = request.session.get('id')
    # # print(user_id)
    # good_id = request.GET.get('goodid')
    # # print(good_id)
    # count = request.GET.get('cartcount')
    # # print(count)
    # user = UserInfo.objects.get(id=user_id)
    # goods = Goods.objects.get(id=good_id)
    # # print(user)
    # # print(goods)
    # if goods:
    #     count = int(count)
    #     order = user.order_set.get(user_id=user_id)

# 方法1
#     new_cart = CartInfo()
#     good_id = request.GET.get('goodid')
#     good_count = request.GET.get('gcount')
#     user_id = request.session.get('id')
#
#     good_ = Goods.objects.filter(id=good_id)
#     user_ = UserInfo.objects.get(id=user_id)
#     # print(good_, user_)
#     if len(good_) > 0:
#         new_cart.user = user_
#         new_cart.good = good_[0]
#     else:
#         return render(request, 'index.html')
#     new_cart.ccount = int(good_count)
#     try:
#         oldgo = CartInfo.objects.filter(user_id=user_id, good_id=good_id)
#         if len(oldgo)>0:
#             oldgo[0].ccount = oldgo[0].ccount + new_cart.ccount
#             oldgo[0].save()
#         else:
#             new_cart.save()
#
#     except DatabaseError as e:
#         logging.warning(e)
#
#     return render(request,'index.html')

# 方法2
    new_cart = CartInfo()
    good_id = request.GET.get('goodid')
    good_count = request.GET.get('gcount')
    user_id = request.session.get('id')

    good_ = Goods.objects.filter(id=good_id)
    user_ = UserInfo.objects.get(id=user_id)
    # print(good_, user_)
    if len(good_) > 0:
        new_cart.user = user_
        new_cart.good = good_[0]
    else:
        content = {'static':'OK','text':'无该商品'}

        return HttpResponse(json.dumps(content))

    new_cart.ccount = int(good_count)
    try:
        oldgo = CartInfo.objects.filter(user_id=user_id, good_id=good_id)
        if len(oldgo)>0:
            oldgo[0].ccount = oldgo[0].ccount + new_cart.ccount
            oldgo[0].save()
        else:
            new_cart.save()

    except DatabaseError as e:
        logging.warning(e)

    # return render(request,'index.html')
    content = {'static': 'OK', 'text': '添加成功'}
    return HttpResponse(json.dumps(content))


def cart_info(request):
    user_id = request.session.get('id')
    find_goods = CartInfo.objects.filter(user_id=user_id)
    print(find_goods)
    return render(request, 'cart.html', {'find_goods':find_goods})

def order(request):
    user_id = request.session.get('id')
    adss = Address.objects.filter(user_id=user_id)
    content = {'adss':adss}
    return render(request, 'order.html', content)

def add_order(request):
    # 获取数据
    # 存数据
    # 返回结果
    user_id = request.session.get('id')
    orderdetail = eval(request.POST.get('acot'))
    adsname = request.POST.get('adsname')
    adsphone = request.POST.get('adsphone')
    ads = request.POST.get('ads')

    acot = 0
    for c in orderdetail:
        acot += int(c['count'])
    print('add_order:',acot)

    acount = 0
    for c in orderdetail:
        acount += eval(c['price'])*int(c['count'])
    orderNO = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    print('add_order:',orderdetail)

    try:
        user = UserInfo.objects.get(id=user_id)
        order = Order.objects.create(orderNO=orderNO, orderdetail=orderdetail,
                                     adsname=adsname, adsphone=adsphone, ads=ads,
                                     acount=acount, acont=acot, user=user)
        print(order)
    except DatabaseError as e:
        logging.warning(e)

    content = {'static':'OK'}

    # ads_id = request.GET.get('ads_id')
    # ads = Address.objects.get(id=ads_id)
    # print(ads)

    return HttpResponse(json.dumps(content))
    # return render(request, 'show_order.html', locals())


def delete_cart(request):
    # 非物里删除
    user_id = request.session.get('id')
    cart_id = request.GET.get('cart_id')
    print(cart_id)
    try:
        delcart = Order.objects.filter(user_id=user_id, id=cart_id)
        delcart[0].delete()
    except DatabaseError as e:
        logging.warning(e)

    # content = {'static':'OK', 'msg':'删除成功'}

    return redirect('/cartinfo/showorder')



def show_order(request):
    user_id = request.session.get('id')
    user = UserInfo.objects.get(id=user_id)
    orders = user.order_set.all()
    print(orders)
    return render(request, 'show_order.html', locals())










