from django.contrib import admin

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice
)


admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(Product)
admin.site.register(ProductPrice)
