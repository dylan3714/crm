#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm, Form
from rbac import models


class RecordForm(ModelForm):
    class Meta:
        model = models.CoustomerRecord
        fields = "__all__"
        exclude = ['delete_status',]

    def __init__(self, request,*args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant=request.user_obj)
            elif name == 'consultant':
                field.choices = ((request.user_obj.pk,request.user_obj.name),)


        self.fields['customer'].empty_label = "请选择客户"




class PaymentUserForm(ModelForm):
    class Meta:
        model = models.CoustomerRecord
        exclude = ['customer',]

    def __init__(self, *args, **kwargs):
        super(PaymentUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
