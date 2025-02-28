from django.db import models
from accounts.models import CustomUser
from django.forms import model_to_dict

class Farm(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="farms")
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        return item
    
    def __str__(self):
        return self.name

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

