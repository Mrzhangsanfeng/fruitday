import random

from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import HttpResponse
from django.db import DatabaseError
import logging


# Create your views here.

def index(request):
    # 方案一
    # 查数据库全部商品
    # 按照分类名查商品,并分别储存传回前端

    # 查商品按固定分类名
    # 返回首页
    try:
        good_fruit_type = get_object_or_404(GoodsType, title='水果')
        print(good_fruit_type)
        fruit_goods = random.sample(list(good_fruit_type.goods_set.all()), 2)


    except DatabaseError as e:
        logging.warning(e)

    # 方法2:
    types = GoodsType.objects.all()
    goods = Goods.objects.all()

    # 方法3
    ac = []
    typess = GoodsType.objects.all()
    for type in typess:
        b = {}
        b['type'] = type.title
        good_type = get_object_or_404(GoodsType, title=type.title)
        f_goods = random.sample(list(good_type.goods_set.all()), 2)
        b['goods'] = f_goods
        ac.append(b)
    print(ac)
    return render(request, 'index.html', locals())

def detail_one(request):
    # 查数据库该id的商品
    # good_id = request.GET.get('goodid')[:-1]
    # print(2222222,good_id)
    good_id = request.GET.get('goodid')
    print(request.GET.get('goodid'))
    print('XXX',request.GET.get('XXX'))
    try:
        goodone = Goods.objects.filter(id=good_id)
    except DatabaseError as e:
        logging.warning(e)
    return render(request, 'detail.html', {'goodone': goodone[0]})






