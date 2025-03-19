from django.db import models
# Create your models here.

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    def __str__(self):
        return self.name

class Variety(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='variety', verbose_name="Cultivo")
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name} ({self.crop.name})"

class AgricultureActivity(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='activity', verbose_name="Cultivo")
    name = models.CharField(max_length=150, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name} - {self.crop.name}"
