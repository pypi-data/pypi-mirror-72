from django.contrib import admin
from .models import DeviceInfo


@admin.register(DeviceInfo)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'mac')