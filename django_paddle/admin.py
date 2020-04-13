from django.contrib import admin
from django_paddle.models import PaddlePlan, PaddleInitialPrice, PaddleRecurringPrice, PaddleSubscription


class PaddleInitialPriceInline(admin.TabularInline):
    model = PaddleInitialPrice


class PaddleRecurringPriceInline(admin.TabularInline):
    model = PaddleRecurringPrice


class PaddlePlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'billing_type', 'billing_period']
    inlines = [PaddleInitialPriceInline, PaddleRecurringPriceInline]


admin.site.register(PaddlePlan, PaddlePlanAdmin)
admin.site.register(PaddleSubscription)
