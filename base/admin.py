from django.contrib import admin
from .models import (
    Sms,
    Comment,
    Rate,
    Favorite,
    Discount,
    Report,
    File
)

admin.site.register(Sms)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Favorite)
admin.site.register(Discount)
admin.site.register(Report)
admin.site.register(File)
