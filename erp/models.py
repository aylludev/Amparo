from django.db import models
from accounts.models import CustomUser
from django.forms import model_to_dict

class Farm(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    country = models.CharField(max_length=100, default="Colombia", verbose_name="Pais")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="Departmento")
    municipality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Municipio")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="farms")
    area = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, verbose_name="Áea")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        return item
    
    def __str__(self):
        return self.name

class Crop(models.Model):
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100, verbose_name="Nombre del cultivo")
    variety = models.CharField(max_length=100, verbose_name="Variedad", blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('perenne', 'Perenne'), ('no_perenne', 'No Perenne')], verbose_name="Tipo")
    area = models.FloatField(verbose_name="Área sembrada (ha)")
    status = models.CharField(max_length=50, choices=[('activo', 'Activo'), ('cosechado', 'Cosechado'), ('en_produccion', 'En Producción')], default='activo', verbose_name="Estado")
    planting_date = models.DateField(verbose_name="Fecha de siembra")
    estimated_harvest_date = models.DateField(verbose_name="Fecha estimada de cosecha", blank=True, null=True)
    observations = models.TextField(verbose_name="Observaciones", blank=True, null=True)

    class Meta:
        verbose_name = "Cultivo"
        verbose_name_plural = "Cultivos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.variety if self.variety else 'Genérico'} ({self.farm.name})"

class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="activities")
    description = models.TextField()
    type = models.CharField(max_length=50)  # Example: 'Planting', 'Harvesting'
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    responsible = models.CharField(max_length=100, blank=True, null=True)  # Could be a worker

    def __str__(self):
        return f"{self.description} - {self.get_status_display()}"

class Supply(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="supplies")
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)  # Example: kg, liters, units

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class Worker(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="workers")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hired_date = models.DateField()

    def __str__(self):
        return self.name

