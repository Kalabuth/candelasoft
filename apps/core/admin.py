from django.contrib import admin

from apps.core.models.suscription import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "start_date", "end_date")