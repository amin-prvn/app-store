from django.contrib import admin

from .models import App, Purchase


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in App._meta.fields if field.name != "id"]
    
    
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Purchase._meta.fields if field.name != "id"]