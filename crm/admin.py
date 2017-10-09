from django.contrib import admin
from crm import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','phone','source','fields','date','status')
    list_filter = ('source','sales','date')
    search_fields = ('fields','name')
    raw_id_fields = ('sales',)
    filter_horizontal = ('tags',)
    list_editable = ('status',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')

admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.Field)
admin.site.register(models.Tag)
admin.site.register(models.District)
admin.site.register(models.VisitList)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.Document)
admin.site.register(models.Menu)
