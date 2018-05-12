from django.contrib import admin
from .models import (
  StoreCategory,
  Store,
  StoreVisit
)


admin.site.register(StoreCategory)
admin.site.register(Store)
admin.site.register(StoreVisit)
