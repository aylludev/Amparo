from django.db import models
# Create your models here.

class CatalogCrop(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"

class CatalogVariety(models.Model):
    crop = models.ForeignKey(CatalogCrop, on_delete=models.CASCADE, related_name='variety', verbose_name="Cultivo")
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"

class CatalogAgricultureActivity(models.Model):
    crop = models.ForeignKey(CatalogCrop, on_delete=models.CASCADE, related_name='activity', verbose_name="Cultivo")
    name = models.CharField(max_length=150, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"

class CatalogAnimal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"

class CatalogRace(models.Model):
    crop = models.ForeignKey(CatalogAnimal, on_delete=models.CASCADE, related_name='variety', verbose_name="Cultivo")
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"

class CatalogAnimalActivity(models.Model):
    crop = models.ForeignKey(CatalogAnimal, on_delete=models.CASCADE, related_name='activity', verbose_name="Cultivo")
    name = models.CharField(max_length=150, verbose_name="Nombre")

    def __str__(self):
        return f"{self.name}"
