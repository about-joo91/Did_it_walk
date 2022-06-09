from django.db import models

# Create your models here.
class Shoes(models.Model):
    class Meta:
        db_table = 'shoes'
    tag_title = models.CharField(max_length=128)
    tag_price = models.CharField(max_length=128)
    tag_image_url = models.URLField(max_length=256)