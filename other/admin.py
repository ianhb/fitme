from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from other.models import *


class FitmeUserInline(admin.StackedInline):
    model = FitMeUser
    can_delete = False
    verbose_name_plural = 'FitMe User'


class UserAdmin(BaseUserAdmin):
    inlines = (FitmeUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(WeightLog)
admin.site.register(BodyFatLog)
