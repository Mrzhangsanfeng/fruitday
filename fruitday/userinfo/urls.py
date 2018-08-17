
from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^register/', register_in, name='register'),
    url(r'^registerin/', register_, name='register_in'),
    url(r'^login/', login_in, name='login'),
    url(r'^loginin/', login_, name='login_in'),
    url(r'^loginout/', login_out, name='login_out'),
    url(r'^delete_ads', delete_ads, name='delete_ads'),
    url(r'^user_ads', user_ads, name='user_ads'),
    url(r'^add_ads', add_ads, name='add_ads'),
    url(r'^myemail', myemail, name='myemail'),
    url(r'^yanzheng', myCaptcha, name='yanzheng'),
    # url(r'^verify_code', verify_code, name='verify_code'),
    url(r'^verify_code/$', verify_code,name='verify_code'),
]
