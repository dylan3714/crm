from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from rbac import models
from django.conf import settings

class UserAuth(MiddlewareMixin):

    def process_request(self,request):
        # print(type(request))
        white_list = settings.WHITE_URL_LIST
        if request.path in white_list:
            return
        user_id = request.session.get('user_id')


        if user_id:
            user_obj = models.User.objects.get(id=request.session.get('user_id'))
            # 将当前登录用户对象作为一个属性，封装给了request
            request.user_obj = user_obj
            return

        else:
            return redirect('web:login')








