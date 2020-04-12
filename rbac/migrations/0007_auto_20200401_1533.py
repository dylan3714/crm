# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-01 07:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, unique=True, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='weight',
            field=models.IntegerField(default=1, verbose_name='权重'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='菜单'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='URL别名'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='父权限'),
        ),
    ]