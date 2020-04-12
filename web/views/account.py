from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from rbac.server.init_permission import init_permission
import copy
from django.contrib import auth
from django.views import View




# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user_obj = models.User.objects.filter(name=username, password=pwd).first()
        if user_obj:

            # 将用户信息保存到session中
            request.session['user_id'] = user_obj.id
            # 权限信息注入到session中
            init_permission(request, user_obj)

            return redirect(reverse('web:customer'))
        else:

            return render(request, 'login.html', {'error': '用户名或者密码错误'})





class LoughtView(View):
    """
    退出登录
    """
    def get(self,request):

        auth.logout(request)

        return redirect(reverse('web:login'))



# def logout_view(request):
#     #清除session，登出
#     auth.logout(request)
#     return render(request,'login.html')



