from contextlib import nullcontext
from django.db import models
from accounts.models import CustomUser
from django.forms import model_to_dict
from catalogs.models import CatalogCrop, CatalogVariety, CatalogAgricultureActivity, CatalogAnimal, CatalogAnimalActivity, CatalogRace
from datetime import datetime
from Amparo import settings
from erp.choices import gender_choices

class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="category")
    name = models.CharField(max_length=150, verbose_name='Nombre')
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="product")
    name = models.CharField(max_length=150, verbose_name='Nombre')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
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

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="client")
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sale")
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
    country = models.CharField(max_length=100, default="Colombia", verbose_name="País")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="Departmento")
    municipality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Municipio")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="farms")
    area = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, verbose_name="Área")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")

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
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
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
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animales"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

class Worker(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="worker")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefono")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salario")
    hired_date = models.DateField(verbose_name="Fecha de contratación")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name

class Suply(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="suply")
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    purchase = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de compra')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['user'])
        item['full_name'] = '{} / {}'.format(self.name, self.cat.name)
        item['cat'] = self.cat.toJSON()
        item['purchase'] = format(self.purchase, '.2f')
        return item

class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completado'),
    ]
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    name = models.ForeignKey(CatalogAgricultureActivity, on_delete=models.CASCADE, related_name='crops', verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    date = models.DateField(verbose_name='Fecha')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Estado')
    workers = models.ManyToManyField(Worker, null=True, blank=True, related_name='activities', verbose_name='Trabajadores')  # Could be a worker
    suplies = models.ManyToManyField(Suply, null=True, blank=True, related_name='activities', verbose_name='Insumos')  # Could be a worker
    cash = models.FloatField(verbose_name='Costo')
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self): return f"{self.description} - {self.get_status_display()}"

    def toJSON(self):
        item = model_to_dict(self, exclude=['crop', 'worker', 'suply'])
        item['crop'] = self.crop.name
        item['suply'] = self.suplies.toJSON()
        item['cash'] = format(self.cash, '.2f')
        return item

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
    workers = models.ManyToManyField(Worker, null=True, blank=True, related_name='Animal_Trabajadores', verbose_name='Trabajadores')  # Could be a worker
    suplies = models.ManyToManyField(Suply, null=True, blank=True, related_name='Animal_Insumos', verbose_name='Insumos',limit_choices_to={'cat__name': 'Insumo'})  # Could be a worker
    cash = models.FloatField(verbose_name='Costo')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    def __str__(self): return f"{self.description} - {self.get_status_display()}"

class Equipment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Relación con usuario
    name = models.CharField(max_length=100, verbose_name='Nombre')  # Nombre del equipo
    desc = models.TextField(blank=True, null=True, verbose_name='Descripción')  # Descripción opcional
    status = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo'), ('en reparación', 'En reparación')],
        default='activo',
        verbose_name='Estado'
    )  # Estado del equipo
    purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Precio de compra')  # Fecha de compra
    costph = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, verbose_name='Costo por Hora')  # Costo del equipo

    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d') if self.purchase_date else None,
            'cost': float(self.cost)  # Convertir Decimal a float
        }

    def __str__(self):
        return self.name
