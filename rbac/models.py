from django.db import models
from django.utils.safestring import mark_safe

class Menu(models.Model):
    """
    一级菜单
    """
    title = models.CharField(max_length=32, unique=True,verbose_name='标题')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    weight = models.IntegerField(default=1,verbose_name='权重')
    
    class Meta:
        verbose_name_plural = '菜单表'
        verbose_name = '菜单表'
    
    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    有关联Menu的是二级菜单
    没有关联Menu的不是二级菜单，是不可以做菜单的权限
    
    
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=32, verbose_name='权限')
    menu = models.ForeignKey('Menu', null=True, blank=True,verbose_name='菜单',on_delete=models.CASCADE)
    
    parent = models.ForeignKey('Permission', null=True, blank=True,verbose_name='父权限',on_delete=models.CASCADE)
    name = models.CharField(max_length=32, null=True, blank=True, unique=True,verbose_name='URL别名')
    
    class Meta:
        verbose_name_plural = '权限表'
        verbose_name = '权限表'
    
    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色所拥有的权限', blank=True)
    
    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField(to='Role', verbose_name='用户所拥有的角色', blank=True)

    def __str__(self):
        return self.name




level_choices = (('a', "未沟通"),
                 ('b', "已沟通第一通电话"),
                 ('c', "已沟通第二通电话"),
                 ('d', "意向客户"),
                 ('e', "成交客户"),
                 )
#客户表
class Customer(models.Model):
    """
    客户表
    """
    level =models.CharField('等级',choices=level_choices,max_length=6,help_text="选择此客户的等级")
    name = models.CharField('姓名', max_length=32, help_text='客户真实姓名') #可为空，有些人就不愿意给自己的真实姓名
    sex_type = (('male', '男'), ('female', '女'))
    sex = models.CharField("性别", choices=sex_type, max_length=16, default='male', blank=True,
                           null=True)  # 存的是male或者female，字符串
    position = models.CharField('职位',max_length=32,blank=True,null=True)
    company = models.CharField('公司名称',max_length=64,unique=True)
    phone = models.CharField('手机号', max_length=16, unique=True)
    wechat = models.CharField('微信',max_length=32,blank=True,null=True)
    remark = models.TextField(verbose_name="备注...",default='无')

    source = models.CharField('客户来源', max_length=128,blank=True,null=True)

    # customer_note = models.TextField("客户备注", blank=True, null=True, )

    date = models.DateTimeField("咨询日期", auto_now_add=True)
    last_consult_date = models.DateField("最后跟进日期", auto_now_add=True) #考核销售的跟进情况，如果多天没有跟进，会影响销售的绩效等
    next_date = models.DateField("预计再次跟进时间", blank=True, null=True) #销售自己大概记录一下自己下一次会什么时候跟进，也没啥用

    #用户表中存放的是自己的客户
    consultant = models.ForeignKey('User', verbose_name="销售人员", related_name='customers', blank=True, null=True,on_delete=models.CASCADE )

    class Meta:
        ordering = ['-id',]
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表'

    def __str__(self):
        return self.name

    def status_show(self):
        status_color = {
            'a':'red',
            'b':'green',
            'c':'orange',
            'd':'yellow',
            'e':'lightblue',
        }

        return mark_safe("<span style='background-color:{0}; padding:5px 18px 5px 18px; border-radius:10%;'>{1}</span>"
                         .format(status_color[self.level],self.level))


seek_status_choices = (('A', '未沟通'), ('B', '已沟通第一通电话'), ('C', '已沟通第二通电话'), ('D', '意向客户'),
                        ('E', '成交客户'),
                       )

class CoustomerRecord(models.Model):
    """
    跟进记录表
    """
    customer = models.ForeignKey('Customer', verbose_name="所咨询客户")
    note = models.TextField(verbose_name="跟进内容...")
    status = models.CharField("跟进状态", max_length=8, choices=seek_status_choices, help_text="选择客户此时的状态",default='A')
    consultant = models.ForeignKey("User", verbose_name="跟进人", related_name='records')
    date = models.DateTimeField("跟进日期", auto_now_add=True)
    delete_status = models.BooleanField(verbose_name='删除状态', default=False)
    # def __str__(self):

    def __str__(self):
        return self.customer.name


    def show_status(self):
        show_color = {
            'A':'red',
            'B':'green',
            'C':'orange',
            'D':'yellow',
            'E':'lightblue',
        }

        return mark_safe("<span style='background-color:{0}; padding:5px 18px 5px 18px; border-radius:10%;'>{1}</span>"
                         .format(show_color[self.status],self.status))


    class Meta:
        ordering = ['id',]
        verbose_name='客户跟进表'
        verbose_name_plural = '客户跟进表'


