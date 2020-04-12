import os
import mimetypes
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from web.utils.page import MyPagenation
from django.views import View
from django.urls import reverse
from django.db.models import Q
# import xlrd

from rbac import models
from web.forms.customer import CustomerForm
from web.forms.customer import CoustomerRecordForm


class Customer_list(View):
    """
    客户列表
    :return:
    """
    def get(self,request):


        user_obj = request.user_obj
        rol = models.User.objects.filter(name=request.user_obj).first().roles.all().first().name

        if rol == 'Boss':
            customer_list = models.Customer.objects.all().reverse()
        else:
            customer_list = models.Customer.objects.filter(consultant=user_obj).reverse()



        # customer_list = models.Customer.objects.filter(consultant=request.user_obj)
        # print('____________________________',request.session['user_id'])
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
        return render(request, 'customer_list.html',
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



#新增客户
def customer_add(request):
    """
    新增客户
    :return:
    """
    if request.method == 'GET':
        form = CustomerForm(request)
        return render(request, 'customer_edit.html', {'form': form})
    form = CustomerForm(request,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_edit.html', {'form': form})


def customer_edit(request, cid):
    """
    编辑客户
    :return:
    """
    obj = models.Customer.objects.get(id=cid)
    if request.method == 'GET':
        form = CustomerForm(request,instance=obj)
        return render(request, 'customer_add.html', {'form': form})
    form = CustomerForm(request,data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/customer/list/')
    return render(request, 'customer_add.html', {'form': form})


def customer_del(request, cid):
    """
    删除客户
    :param request:
    :param cid:
    :return:
    """
    models.Customer.objects.filter(id=cid).delete()
    return redirect('/customer/list/')




class AddEditConsultView(View):

    def get(self,request,cid=None):

        """
            添加客户和编辑客户
            :param request:
            :param cid:   客户记录id
            :return:
            """
        label = '编辑跟进记录' if cid else '添加跟进记录'
        consult_obj = models.CoustomerRecord.objects.filter(pk=cid).first()

        if request.method == 'GET':
            consult_form = CoustomerRecordForm(request,instance=consult_obj)
            return render(request, 'add_edit_consult.html', {'consult_form': consult_form, 'label': label})

    def post(self,request,cid=None):
        consult_obj = models.CoustomerRecord.objects.filter(pk=cid).first()
        next_url = request.GET.get('next')
        if not next_url:
            next_url = reverse('consult_record')
        consult_form = CoustomerRecordForm(request,request.POST, instance=consult_obj)
        if consult_form.is_valid():
            consult_form.save()

            return redirect(next_url)
        else:
            return render(request, 'edit_customer.html', {'consult_form': consult_form,})











