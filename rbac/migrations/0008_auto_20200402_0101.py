# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-01 17:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_auto_20200401_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoustomerRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(verbose_name='跟进内容...')),
                ('status', models.CharField(choices=[('A', '近期无想法'), ('B', '打算找顾问，还未定'), ('C', '已有企业顾问'), ('D', '不打算找顾问')], default='A', help_text='选择客户此时的状态', max_length=8, verbose_name='跟进状态')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='跟进日期')),
                ('delete_status', models.BooleanField(default=False, verbose_name='删除状态')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='rbac.User', verbose_name='跟进人')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')], help_text='选择此客户的等级', max_length=6, verbose_name='等级')),
                ('name', models.CharField(help_text='客户真实姓名', max_length=32, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], default='male', max_length=16, null=True, verbose_name='性别')),
                ('position', models.CharField(blank=True, max_length=32, null=True, verbose_name='职位')),
                ('company', models.CharField(max_length=64, unique=True, verbose_name='公司名称')),
                ('phone', models.CharField(max_length=16, unique=True, verbose_name='手机号')),
                ('wechat', models.CharField(blank=True, max_length=32, null=True, verbose_name='微信')),
                ('source', models.CharField(blank=True, max_length=128, null=True, verbose_name='客户来源')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
                ('next_date', models.DateField(blank=True, null=True, verbose_name='预计再次跟进时间')),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='rbac.User', verbose_name='销售人员')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(verbose_name='付费金额')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='付费时间')),
            ],
        ),
        migrations.AddField(
            model_name='coustomerrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Customer', verbose_name='所咨询客户'),
        ),
    ]