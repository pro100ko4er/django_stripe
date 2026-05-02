from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()

class Discount(models.Model):
    name = models.CharField(max_length=255)
    stripe_coupon_id = models.CharField(max_length=255)

class Tax(models.Model):
    name = models.CharField(max_length=255)
    stripe_tax_id = models.CharField(max_length=255)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def total_amount(self):
        return sum(item.price for item in self.items.all())