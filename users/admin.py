from django.contrib import admin

from .models import User, UpgradeRequest

admin.site.register(User)
admin.site.register(UpgradeRequest)
