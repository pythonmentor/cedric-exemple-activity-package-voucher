from django.contrib import admin

from .models import Product, Activity, Package, Voucher, OrderLine

admin.site.register(Product)
admin.site.register(Activity)
admin.site.register(Package)
admin.site.register(Voucher)
admin.site.register(OrderLine)
