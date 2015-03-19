from django.db import models

class List(models.Model):
    pass

# classes inheriting from models.Model map to tables in the db
class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

