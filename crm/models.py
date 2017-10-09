from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
# Create your models here.


class Customer(models.Model):
    '''客户信息表'''
    name = models.CharField(max_length=32,blank=True,null=True)
    email = models.EmailField(max_length=64,unique=True,blank=True,null=True)
    phone = models.CharField(max_length=64,blank=True,null=True)
    source_choices = ((0,'转介绍'),
                      (1,'自主开发'),
                      (2,'总部资源'),
                      )
    source = models.SmallIntegerField(choices=source_choices,default=0)
    referral_from = models.CharField(verbose_name="转介绍人姓名",max_length=64,blank=True,null=True)

    fields = models.ForeignKey('Field' ,verbose_name="细分领域")
    content = models.TextField(verbose_name="基本沟通内容介绍")
    tags = models.ManyToManyField("Tag",blank=True,null=True)
    status_choices = ((0,'有意向'),
                      (1,'无意向'),
                      (2,'未沟通'),
                      (3,'已签约'),
                      )
    status = models.SmallIntegerField(choices=status_choices,default=0)
    sales = models.ForeignKey("UserProfile")
    memo = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ="客户表"
        verbose_name_plural ="客户表"#使admin中显示为客户表而不是客户表s

class Field(models.Model):
    '''产出线,目标销售额，销售周期，简介'''
    field_choice=((0,'PTN'),
                  (1,'OTN'),
                  (2,'CTrans'),
                  (3,'路由器'),
                  (4,'其他'),
                  )
    fields = models.SmallIntegerField(choices= field_choice,default=0,verbose_name='产出线')
    target_revenue = models.PositiveSmallIntegerField(verbose_name="预期销售额")
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField()

    def __int__(self):
        return self.fields

    class Meta:
        verbose_name = "产出线"
        verbose_name_plural = "产出线"

class Tag(models.Model):
    name = models.CharField(unique=True,max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

class District(models.Model):
    '''地区'''
    name = models.CharField(max_length=128,unique=True)
    addr = models.CharField(max_length=128)
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "地区"
        verbose_name_plural = "地区"

class VisitList(models.Model):
    '''客户拜访表'''
    district = models.ForeignKey("District",verbose_name="地区")
    visit_fields = models.ForeignKey("Field")
    CRM_type_choices = ((0,'陌拜'),
                          (1,'宴请'),
                          (2,'家访'),
                          (3,'招投标'),
                          (4,'娱乐活动'),
                          )
    CRM_type = models.SmallIntegerField(choices=CRM_type_choices,verbose_name="客户拜访类型")
    sales = models.ManyToManyField("UserProfile")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期",blank=True,null=True)

    def __str__(self):
        return "%s %s %s" %(self.sales,self. visit_fields,self.CRM_type_choices)

    class Meta:
        verbose_name_plural = "拜访表"
        verbose_name = "拜访表"

class UserProfile(models.Model):
    '''账号表'''
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role",blank=True,null=True)


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "客户经理"
        verbose_name_plural = "客户经理"

class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32,unique=True)
    menus = models.ManyToManyField("Menu",blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "角色"

class Document(models.Model):
    '''签单表'''
    customer = models.ForeignKey("Customer")
    document_class = models.ForeignKey("VisitList",verbose_name="签单类型")
    sales = models.ForeignKey("UserProfile",verbose_name="销售员")
    contract_approved = models.BooleanField(default=False,verbose_name="合同已审核")
    amount = models.PositiveIntegerField(verbose_name="合同额",blank=not contract_approved,null=not contract_approved)
    contract_num = models.CharField(max_length=32,blank=not contract_approved,null=not contract_approved)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.document_class)

    class Meta:
        verbose_name_plural = "签单表"

class Payment(models.Model):
    '''付款记录'''
    customer = models.ForeignKey("Customer")
    course = models.ForeignKey("Field",verbose_name="产出线")
    amount = models.PositiveIntegerField(verbose_name="应收数额",default=0)
    payment_amount = models.PositiveIntegerField(verbose_name='已付款')
    sales = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.amount)

    class Meta:
        verbose_name_plural = "付款记录"

class Menu(models.Model):
    '''菜单'''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
