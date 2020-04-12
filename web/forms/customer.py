#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from rbac import models
from django import forms


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"



    def __init__(self, request,*args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if name == 'consultant':
                field.choices = ((request.user_obj.pk,request.user_obj.name),)

        self.fields['level'].empty_label = "请选择客户目前状态"

class CoustomerRecordForm(forms.ModelForm):

    class Meta:
        model = models.CoustomerRecord
        fields = '__all__'
        exclude = ['delete_status',]

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            print(field_name,field)
            field.widget.attrs.update({'class':'form-control'})
            if field_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant=request.user_obj)
            elif field_name == 'consultant':
                # field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.pk)
                field.choices = ((request.user_obj.pk,request.user_obj.username),)