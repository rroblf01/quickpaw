from django.contrib import admin
from django.http import HttpRequest

from .models import Amount, Bill, Category, ItemSolded, Product


class AmountInline(admin.TabularInline):  # type: ignore
    model = Amount
    extra = 1


class ProductAdmin(admin.ModelAdmin):  # type: ignore
    inlines = [AmountInline]


class ItemSoldedInline(admin.TabularInline):  # type: ignore
    model = ItemSolded
    extra = 1
    readonly_fields = [field.name for field in ItemSolded._meta.fields]

    def has_add_permission(
        self, request: HttpRequest, obj: ItemSolded | None = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: ItemSolded | None = None
    ) -> bool:
        return False


class BillAdmin(admin.ModelAdmin):  # type: ignore
    inlines = [ItemSoldedInline]
    readonly_fields = [field.name for field in Bill._meta.fields]

    def has_add_permission(self, request: HttpRequest, obj: Bill | None = None) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Bill | None = None
    ) -> bool:
        return False


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Bill, BillAdmin)
