from django.db import models

# classes inheriting from models.Model map to tables in the db
class Item(models.Model):
    text = models.TextField(default='')
