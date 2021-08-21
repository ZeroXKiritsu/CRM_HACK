from django.contrib import admin
from .models import Account

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('status',)

admin.site.register(Account, AccountAdmin)