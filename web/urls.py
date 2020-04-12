from django.conf.urls import url
from web.views import customer
from web.views import record
from web.views import account
app_name = 'web'
urlpatterns = [
    
    url(r'^customer/list/$', customer.Customer_list.as_view(), name='customer'),
    url(r'^customer/add/$', customer.customer_add, name='customer_add'),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit, name='customer_edit'),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del, name='customer_del'),

    # 跟进记录展示
    # url(r'^consult_record/', customer.ConsultRecordView.as_view(),name='consult_record'),
    # url(r'^consult_record/(?P<cid>\d+)/', record.ConsultRecordView.as_view, name='consult_record'),


    # url(r'^edit_consult_record/(\d+)/', customer.AddEditConsultView.as_view(),name='edit_consult_record'),

    url(r'^record/list/', record.ConsultRecordView.as_view(), name='record'),
    url(r'^record/add/', record.AddEditConsultView.as_view(), name='record_add'),
    # url(r'^record/add/(?P<pid>\d+)/$', record.AddEditConsultView.as_view(), name='my_record_add'),
    # url(r'^record/add/$', record.AddEditConsultView.as_view(), name='payment_add'),
    url(r'^record/edit/(?P<pid>\d+)/$', record.AddEditConsultView.as_view(), name='record_edit'),
    url(r'^record/del/(?P<pid>\d+)/$', record.record_del, name='record_del'),
    
    url(r'^login/$', account.login,name='login'),
    url(r'^logout/$', account.LoughtView.as_view(),name='logout')
]
