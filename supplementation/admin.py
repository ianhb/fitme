# Register your models here.
from django.contrib import admin

from supplementation.models import *

admin.site.register(Supplement)
admin.site.register(SupplementLog)
admin.site.register(SupplementCategory)
admin.site.register(Brand)
