from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'category'


class Product(models.Model):
    SIZE_CHOICE = (
        ('small', 'small'),
        ('large', 'large')
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    cost = models.IntegerField()
    name = models.CharField(max_length=3 * 20, db_index=True)
    name_jamo = models.CharField(max_length=3 * 20, db_index=True)
    content = models.TextField(max_length=3 * 100)
    barcode = models.CharField(max_length=13)
    expire = models.DateField()
    size = models.CharField(max_length=10, choices=SIZE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'product'
