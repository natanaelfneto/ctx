from django.contrib import admin

from .models import *

admin.site.register(Address)
admin.site.register(Equipment)
admin.site.register(Client)
admin.site.register(Supply)
admin.site.register(Invoice)

