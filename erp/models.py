from django.db import models
from accounts.models import CustomUser
from django.forms import model_to_dict
from catalogs.models import CatalogCrop, CatalogVariety, CatalogAgricultureActivity, CatalogAnimal, CatalogAnimalActivity, CatalogRace
from datetime import datetime
from Amparo import settings
from erp.choices import gender_choices

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    purchase = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de compra')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['purchase'] = format(self.pvp, '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cedula')
    email = models.EmailField(max_length=254, null=True, blank=True, unique=True, verbose_name='Correo electrónico')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=150, null=True, blank=True, verbose_name='Ciudad')
    cellphone = models.CharField(max_length=150, null=True, blank=True, verbose_name='Telefono')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    observation = models.CharField(max_length=254, null=True, blank=True, verbose_name='Observaciones')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    TYPE_PAYMENT = [
        ('CREDIT', 'Crédito'),
        ('CASH', 'Contado'),
    ]

    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    discountall = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    type_payment = models.CharField(max_length=10, choices=TYPE_PAYMENT, default='CREDIT')
    down_payment = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    observation = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['discountall'] = format(self.discountall, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['type_payment'] = self.type_payment
        item['down_payment'] = format(self.down_payment, '.2f')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detsale_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['date_joined']


class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(0)
    discount = models.IntegerField(0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class CreditSale(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="credit_sale")
    total_credit = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pendiente'), ('paid', 'Pagado')], default='pending')

    def total_paid(self):
        """Calcula el saldo pendiente del crédito."""
        total_paid = self.down_payment + sum(self.payments.values_list('amount', flat=True))
        return total_paid
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['names'] = self.sale.cli.names
        item['lastnames'] = self.sale.cli.surnames,
        item['date_joined'] = self.sale.date_joined.strftime('%Y-%m-%d')
        item['total_credit'] = float(self.total_credit)
        item['total_paid'] = float(self.total_paid())
        item['pending_balance'] = float(self.total_credit - self.total_paid())
        return item

    def __str__(self):
        return f"Crédito #{self.sale.id} - {self.sale.cli}"

class CreditPayment(models.Model):
    credit_sale = models.ForeignKey(CreditSale, on_delete=models.CASCADE, related_name="payments")
    date = models.DateTimeField(default=datetime.now, verbose_name="Fecha de pago")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Abono")

    def __str__(self):
        return f"Pago de ${self.amount} - {self.credit_sale.sale.cli} - {self.date}"

class Cotization(models.Model):
    TYPE_PAYMENT = [
        ('CONTADO', 'Contado'),
        ('CREDITO', 'Credito'),
    ]

    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    discountall = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    type_payment = models.CharField(max_length=10, choices=TYPE_PAYMENT, default='CONTADO')
    down_payment = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['discountall'] = format(self.discountall, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['type_payment'] = self.type_payment
        item['det'] = [i.toJSON() for i in self.detcotization_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detcotization_set.all():
            det.prod.stock += det.cant
            det.prod.save()
        super(Cotization, self).delete()

    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['id']

class DetCotization(models.Model):
    cotization = models.ForeignKey(Cotization, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['cotization'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Cotizacion'
        verbose_name_plural = 'Detalle de Cotizaciones'
        ordering = ['id']

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
    name = models.ForeignKey(CatalogCrop, on_delete=models.CASCADE, related_name='crops', verbose_name='Nombre')
    variety = models.ForeignKey(CatalogVariety, on_delete=models.CASCADE, related_name='crops', verbose_name='Variedad')
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

class Animal(models.Model):
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='animal')
    name = models.CharField(max_length=100, verbose_name="Nombre del Animal")
    type = models.ForeignKey(CatalogAnimal, on_delete=models.CASCADE, verbose_name="Tipo")
    raza = models.ForeignKey(CatalogRace, on_delete=models.CASCADE, verbose_name="Raza", blank=True, null=True)
    birthday_date = models.DateField(verbose_name="Fecha de nacimiento")

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animales"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class Worker(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hired_date = models.DateField()

    def __str__(self):
        return self.name

class Supply(models.Model):
    name = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('fertilizante', 'Fertilizante'),
        ('pesticida', 'Pesticida'),
        ('alimento', 'Alimento para animales'),
        ('semilla', 'Semilla'),
        ('medicamento', 'Medicamento para animales'),
        ('otros', 'Otros')
    ], default='fertilizante')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)  # Example: kg, liters, units

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
    ]
    
    crop = models.ForeignKey('Crop', on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    name = models.ForeignKey(CatalogAgricultureActivity, on_delete=models.CASCADE, related_name='crops', verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    date = models.DateField(verbose_name='Fecha')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    workers = models.ManyToManyField(Worker, related_name='Trabajadores', verbose_name='Trabajadores')  # Could be a worker
    suplies = models.ManyToManyField(Product, related_name='Insumos', verbose_name='Insumos',limit_choices_to={'cat__name': 'Insumos'})  # Could be a worker
    cash = models.FloatField(verbose_name='Costo')

    def __str__(self): return f"{self.description} - {self.get_status_display()}"

class ActivityAnimal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
    ]
    
    crop = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    name = models.ForeignKey(CatalogAnimalActivity, on_delete=models.CASCADE, related_name='crops', verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    date = models.DateField(verbose_name='Fecha')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    workers = models.ManyToManyField(Worker, related_name='Animal_Trabajadores', verbose_name='Trabajadores')  # Could be a worker
    suplies = models.ManyToManyField(Product, related_name='Animal_Insumos', verbose_name='Insumos',limit_choices_to={'cat__name': 'Insumo'})  # Could be a worker
    cash = models.FloatField(verbose_name='Costo')
    
    def __str__(self): return f"{self.description} - {self.get_status_display()}"
