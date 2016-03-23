from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from other.models import *


class FitKickUserInline(admin.StackedInline):
    model = FitKickUser
    can_delete = False
    verbose_name_plural = 'FitKick Users'


class UserAdmin(BaseUserAdmin):
    inlines = (FitKickUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(WeightLog)
admin.site.register(BodyFatLog)
