from django.contrib import admin

from farmer.models import Farmer, FarmerArea, Report


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'username')


@admin.register(FarmerArea)
class FarmerAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'farmer__name')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('area', 'sensor_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('area__name', 'sensor_id')
