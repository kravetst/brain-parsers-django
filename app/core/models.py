from django.db import models
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    memory = models.CharField(max_length=50, null=True, blank=True)

    price = models.IntegerField(null=True, blank=True)
    sale_price = models.IntegerField(null=True, blank=True)

    images = ArrayField(models.URLField(), null=True, blank=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    reviews_count = models.IntegerField(null=True, blank=True)

    screen_diagonal = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=50, null=True, blank=True)

    specs = models.JSONField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    status = models.CharField(max_length=20, default="New")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    raw_jsonld = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title or "No Title"
