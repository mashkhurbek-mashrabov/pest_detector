from django.db import models


class Farmer(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FarmerArea(models.Model):
    name = models.CharField(max_length=100)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='areas')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    area = models.ForeignKey(FarmerArea, on_delete=models.CASCADE, related_name='reports')
    sensor_id = models.CharField(max_length=100)
    image = models.ImageField(upload_to='reports')
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.area
