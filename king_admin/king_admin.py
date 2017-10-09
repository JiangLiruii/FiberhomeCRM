from crm import models


enabled_admins = {}

class BaseAdmin(object):
    list_display = ()
    list_filters = ()
    list_per_page = 20

class CustomerAdmin(BaseAdmin):
    list_display = ('id','name','email','phone','source','fields','date','tags')
    list_filters = ('source','sales','date','status')
    #model = models.Customer

class SalesAdmin(BaseAdmin):
    list_display = ('customer','name','Document.sales','Payment.sales')


def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:#model_class._meta.app_label 获取app名
        enabled_admins[model_class._meta.app_label] = {} #enabled_admins['crm'] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class #绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class#model_class._meta.model_name为表名
    #enabled_admins['crm']['customerfollowup'] = CustomerFollowUpAdmin


register(models.Customer,CustomerAdmin)
register(models.UserProfile,SalesAdmin)



