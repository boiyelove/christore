from django.contrib import admin

# Register your models here.
from .models import Basket, BasketItem

class BasketAdmin(admin.ModelAdmin):
	class Meta:
		model = Basket


admin.site.register(Basket, BasketAdmin)