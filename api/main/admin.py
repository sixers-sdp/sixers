from django.contrib import admin
from . import models
from . import sync_to_echo


class ProductCategoryAdmin(admin.ModelAdmin):
    actions = ['push_to_echo_dot']

    def push_to_echo_dot(modeladmin, request, queryset):
        sync_to_echo.sync_selected(queryset)


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


class DotAdmin(admin.ModelAdmin):
    pass


class MapAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.DotAssociation, DotAdmin)
admin.site.register(models.CafeMap, MapAdmin)
