from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import RESTRICT


class MetaModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Manufacurer(MetaModel):
    name = models.CharField(max_length=128,null=False,blank=False)

    class Meta:
        db_table = 'manufactorer'

    def __str__(self):
        return self.name

class Laptop(MetaModel):
    manufacturer = models.ForeignKey(Manufacurer,on_delete=RESTRICT,null=False,blank=False)
    product = models.CharField(max_length=512,null=False,blank=False)
    type = models.CharField(max_length=128,null=False,blank=False)
    inches = models.FloatField(null=False,blank=False)
    screen_width = models.IntegerField(null=False,blank=False)
    screen_height = models.IntegerField(null=False,blank=False)
    cpu = models.CharField(max_length=512,null=False,blank=False)
    ram = models.IntegerField(null=False,blank=False)
    memory1_storage = models.CharField(max_length=128,null=True,blank=True)
    memory1_type = models.CharField(max_length=128,null=True,blank=True)
    memory1_GOT = models.CharField(null=True,blank=True,max_length=128)
    memory2_storage = models.CharField(max_length=128,null=True,blank=True)
    memory2_type = models.CharField(max_length=128,null=True,blank=True)
    memory2_GOT = models.CharField(null=True, blank=True, max_length=128)
    gpu = models.CharField(max_length=512,null=False,blank=False)
    os = models.CharField(max_length=128,null=False,blank=False)
    weight_kg = models.CharField(max_length=128,null=False,blank=False)
    price_euro = models.FloatField(null=False,blank=False)
    stock_amount = models.IntegerField(max_length=128,null=False,blank=False,validators=([MinValueValidator(0), MaxValueValidator(100)]))

    class Meta:
        db_table = 'laptops'

    def __str__(self):
        return self.product

class Customer(MetaModel):
    name = models.CharField(max_length=512,null=False,blank=False)
    address = models.CharField(max_length=512,null=False,blank=False)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.name

class Order(MetaModel):
    customer = models.ForeignKey(Customer,on_delete=RESTRICT)
    order_date = models.DateField(null=False,blank=False)
    is_cancelled = models.BooleanField(default=False)
    order_laptops = models.ManyToManyField(through='OrderItems',to=Laptop)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"{self.customer} at {self.order_date}"

class OrderItems(MetaModel):
    order = models.ForeignKey(Order,on_delete=RESTRICT)
    laptop = models.ForeignKey(Laptop,on_delete=RESTRICT)
    item_price = models.FloatField(null=False,blank=False)
    amount = models.IntegerField(null=False,blank=False)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f"{self.order} {self.amount} {self.laptop}"



