from decimal import Decimal
from enum import Enum
from typing import Any, Tuple

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models


class CurrencyChoices(Enum):
    EUR = "EUR", "Euro"
    USD = "USD", "United States Dollar"
    JPY = "JPY", "Japanese Yen"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.value[0], choice.value[1]) for choice in cls]


def product_image_upload_to(instance: models.Model, filename: str) -> str:
    return f"product/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_upload_to)
    categories = models.ManyToManyField(Category, related_name="products")

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk:
            old_image = (
                Product.objects.filter(pk=self.pk)
                .values_list("image", flat=True)
                .first()
            )
            if old_image and old_image != self.image.name:
                default_storage.delete(old_image)
        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Tuple[int, dict[str, int]]:
        if self.image:
            default_storage.delete(self.image.name)
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"Product {self.pk}: {self.name}"


class Amount(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices(),
        default=CurrencyChoices.EUR.value[0],
    )
    size = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="amounts"
    )

    class Meta:
        unique_together = ("product", "size")

    def __str__(self) -> str:
        return f"Amount for {self.product.name}"


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Bill {self.pk} for {self.user.username}"


class ItemSolded(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices(),
        default=CurrencyChoices.EUR.value[0],
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0"))
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return f"Item {self.pk} for Bill {self.bill.pk}"
