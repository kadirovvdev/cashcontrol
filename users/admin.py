from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'phone_number', 'image')
#     search_fields = ('username', 'email')
#     list_filter = ('username', 'email')
#     ordering = ('id',)
