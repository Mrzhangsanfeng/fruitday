import json

import time
from io import BytesIO

from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.db import DatabaseError
import logging
import re

from captcha.image import ImageCaptcha
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import random
import os
# Create your views here.

def register_in(request):
    return render(request, 'register.html')

def register_(request):
    # 获取注册信息
    # 判断用户是否存在
    # 注册用户
    # 返回页面
    if request.method == 'POST':
        new_user = UserInfo()
        new_user.uname = request.POST['user_name'] # 获取用户名
        a = UserInfo.objects.filter(uname=new_user.uname)  # 数据库
        if len(a) > 0:
            return render(request, 'register.html', {'message': '该用户名存在'})
        else:
            upwd = request.POST.get('user_pwd', 'abc')
            ucpwd = request.POST['user_cpwd']
            if upwd == ucpwd:
                new_user.email = request.POST['emial']

                new_user.phone = request.POST['phone']
                new_user.upassword = make_password(upwd, 'abc', 'pbkdf2_sha1')

                # print(make_password('qwe', 'abc', 'pbkdf2_sha1'))
                # print(make_password('qwe', 'abc', 'pbkdf2_sha1'))
                # print(make_password('qwe', 'def', 'pbkdf2_sha1'))
                # print(make_password('qwe', None, 'pbkdf2_sha1'))
                # print(make_password('qwe', None, 'pbkdf2_sha1'))
                # print(make_password('rty', 'abc', 'pbkdf2_sha1'))

                try:
                    new_user.save()
                except DatabaseError as e:
                    logging.warning(e)
                return redirect('/')
            else:
                return render(request, 'register.html', {'message': '两次密码不一致'})

def myemail(request):
    email = request.POST.get('email')
    p = re.compile(r"^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$")
    if re.fullmatch(p, email):
        content = {'msg': ''}
    else:
        content = {'msg':'邮箱错误'}
    # print(json.dumps(content))
    return HttpResponse(json.dumps(content))


def login_in(request):
    print(l)
    return render(request, 'login.html')

def login_(request):
    # 获取用户信息
    # 判断用户信息是否存在
    # 用户登录
    # 返回页面

    if request.method == 'POST':
        uname = request.POST.get('user_name')
        upwd = request.POST.get('user_pwd')
        text_captcha_val = request.POST.get('text_captcha', '')
        # print(text_captcha_val.upper(),222222222222222)
        # print(l[-1][-1].upper(),1111111111111)
        try:
            name_xinxi = UserInfo.objects.filter(uname=uname)
            if len(name_xinxi) > 0:
                if check_password(upwd, name_xinxi[0].upassword):
                    if text_captcha_val.upper() == l[-1][-1].upper():
                        request.session['uname'] = uname
                        request.session['id'] = name_xinxi[0].id

                        request.session.set_expiry(0)

                        # print(l[-1])
                        for d in dict(l).keys():
                            try:
                                os.remove(d)
                            except FileNotFoundError:
                                continue
                        l.clear()

                        return redirect('/')
                    else:
                        return render(request, 'login.html', {'message': '验证码错误'})
                else:
                    return render(request, 'login.html', {'message': '密码错误'})
            else:
                return render(request, 'login.html', {'message':'用户不存在'})
        except DatabaseError as e:
            logging.warning(e)

    elif request.method == 'GET':
        uname = request.session.get('uname', None)
        name_xinxi = UserInfo.objects.filter(uname=uname)
        if len(name_xinxi) > 0:
            return render(request, 'index.html')
        else:
            return redirect('/user/login')

l = []
def myCaptcha(request):
      # 收集验证码文件名

    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ALPH = []
    alph = []
    for i in range(65, 91):
        ALPH.append(chr(i))

    for i in ALPH:
        alph.append(i.swapcase())

    charset = number + alph + ALPH
    text = random.sample(charset, 4)
    text = ''.join(text)

    image = ImageCaptcha()
    captcha = image.generate(text)

    captcha_image = Image.open(captcha)

    captcha_image = np.array(captcha_image)
    plt.imshow(captcha_image)
    # plt.show()
    filename = 'static/captcha/' + str(time.time()) + '.png'
    plt.imsave(filename, captcha_image)
    image_js = {'img':filename}
    image_json = json.dumps(image_js)


    l.append((filename, text))
    return HttpResponse(image_json)

def verify_code(request):
    # 1，定义变量，用于画面的背景色、宽、高
    # random.randrange(20, 100)意思是在20到100之间随机找一个数
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 159)
    width = 100
    height = 30
    # 2，创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 3，创建画笔对象
    draw = ImageDraw.Draw(im)
    # 4，调用画笔的point()函数绘制噪点，防止攻击
    for i in range(0, 100):
    # 噪点绘制的范围
        xy = (random.randrange(0, width), random.randrange(0, height))
        # 噪点的随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        # 绘制出噪点
        draw.point(xy, fill=fill)
        # 5，定义验证码的备选值
    str1 = 'ABCD123EFGHJK456LMNPQRS789TUVWXYZ0'
        # 6，随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 7，构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # arial.ttf window下的字体
    font = ImageFont.truetype('arial.ttf', 23)
    # 8，构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 9，绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 9，用完画笔，释放画笔
    del draw
    # 10，存入session，用于做进一步验证
    request.session['verifycode'] = rand_str.lower()
    # 11，内存文件操作
    buf = BytesIO()
    # 12，将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 13，将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')















def login_out(request):
    try:
        if request.session['uname']:
            del request.session['uname']
            del request.session['id']
    except KeyError as e:
        logging.warning(e)
    return redirect('/')

def add_ads(request):
    # 获取用户(sseion中获取)
    # 获取前端页面传过来的信息(收件人姓名,地址,电话)
    # 对数据库增加操作
    # 返回页面

    if request.method == 'GET':
        return render(request, 'add_ads.html')
    else:
        a = Address()
        a.user_id = request.session.get('id')
        a.aname = request.POST.get('aname')
        a.ads = request.POST.get('ads')
        a.phone = request.POST.get('phone')

        try:
            a.save()
        except DatabaseError as e:
            logging.warning(e)

        return redirect('/user/user_ads')

def user_ads(request):
    # 获取用户id(session中)
    # 查询数据库Address表中用户的id的数据
    # 返回页面
    # user_id = request.session.get('id')
    # user = UserInfo.objects.get(id=user_id)
    # ads = user.address_set.all()
    # # xxx = Address.objects.values('user_id')
    # # print(xxx)
    # # YYY = Address.objects.filter(user_id=9)
    # # print(YYY)
    # return render(request, 'ads.html', locals())

    user_id = request.session.get('id')
    adss = Address.objects.filter(user_id=user_id)
    content = {'adss':adss}
    return render(request, 'order.html', content)





def delete_ads(request):
    # 获取用户id
    # 获取地址id
    # 查询数据库
    # 删除数据库
    # 返回页面
    user_id = request.session.get('id')
    adsid = request.GET.get('adsid')
    try:
        delads = Address.objects.get(id=adsid, user_id=user_id)
        print(delads)
        delads.delete()
    except DatabaseError as e:
        logging.warning(e)
    return redirect('/user/user_ads')



# def delete_session(request):
#     print('close', 1111111111111111111111)
#     msg = request.POST.get('closeSession')
#     if msg == 'ok':
#         del request.session['id']
#         del request.session['uname']
#     resp =  HttpResponse('OK')
#     print(request.COOKIES)
#     resp.delete_cookie('sessionid')
#     del request.COOKIES['sessionid']
#     return resp














