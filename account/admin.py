from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


UserAdmin.fieldsets += (
        _('Formaloo'), {'fields': 
            ('credit',)
        }   
    ),       
admin.site.register(User, UserAdmin)