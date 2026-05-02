from django.contrib import admin

from .models import Item, Discount, Tax, Order

admin.site.register([Item, Discount, Tax, Order])

