#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect,reverse
from django.conf import settings
from web.utils.page import MyPagenation
from django.db.models import Q
from django.views import View

from rbac import models
from web.forms.record import RecordForm, PaymentUserForm


# def payment_list(request):
#     """
#     付费列表
#     :return:
#     """
#     data_list = models.CoustomerRecord.objects.all()

class ConsultRecordView(View):


    def get(self,request):
        rol = models.User.objects.filter(name=request.user_obj).first().roles.all().first().name

        cid = request.GET.get('cid')
        # 如果存在cid，那么找的是单个客户的跟进记录
        if cid:
            customer_list = models.CoustomerRecord.objects.filter(consultant=request.user_obj,
                                                               customer_id=cid)
        elif rol == 'Boss':
            customer_list = models.CoustomerRecord.objects.all()
        else:
            customer_list = models.CoustomerRecord.objects.filter(consultant=request.user_obj)

        # customer_list = models.CoustomerRecord.objects.filter(consultant=request.user_obj)

        get_data = request.GET.copy()  # 将request.GET对象改成可修改的
        page_num = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 选择查询的字段,name
        kw = request.GET.get('kw')  # 查询关键字  #思宇

        if kw:
            kw = kw.strip()
            q_obj = Q()
            q_obj.children.append((search_field, kw))
            # q_obj.children.append(Q(qq_contains='111'))
            customer_list = customer_list.filter(q_obj)

        else:
            customer_list = customer_list
        base_url = request.path  # 访问的路径

        customer_count = customer_list.count()

        per_page_num = settings.PER_PAGE_NUM  # 每页显示多少条数据
        page_num_show = settings.PAGE_NUM_SHOW  # 显示的页码数

        page_obj = MyPagenation(page_num, customer_count, base_url, get_data, per_page_num, page_num_show, )

        page_html = page_obj.page_hmtl()

        customer_objs = customer_list.reverse()[page_obj.start_data_num:page_obj.end_data_num]
        return render(request, 'consultrecord.html',
                      {'data_list': customer_objs, 'page_html': page_html,'role':rol})


    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if hasattr(self,action):

            print(cids)
            ret = getattr(self,action)(request,cids)
            if ret:
                return ret

            return redirect(request.path)




class AddEditConsultView(View):

    def get(self,request,pid=None):

        """
            添加客户和编辑客户
            :param request:
            :param cid:   客户记录id
            :return:
            """
        label = ' 编辑跟进记录' if pid else ' 添加跟进记录'
        consult_obj = models.CoustomerRecord.objects.filter(id=pid).first()

        if request.method == 'GET':
            consult_form = RecordForm(request,instance=consult_obj)
            return render(request, 'record_add_edit.html', {'form': consult_form, 'label': label})

    def post(self,request,pid=None):
        consult_obj = models.CoustomerRecord.objects.filter(pk=pid).first()
        next_url = request.GET.get('next')
        if not next_url:
            next_url = reverse('web:record')
        consult_form = RecordForm(request,request.POST, instance=consult_obj)
        if consult_form.is_valid():
            consult_form.save()

            return redirect(next_url)
        else:
            return render(request, 'record_add_edit.html', {'form': consult_form,})



def record_del(request, pid):
    """
    删除跟进记录
    :param request:
    :param cid:
    :return:
    """
    models.CoustomerRecord.objects.filter(id=pid).delete()
    return redirect('/record/list/')

