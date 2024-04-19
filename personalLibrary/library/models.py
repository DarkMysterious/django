from django.db import models

class Book(models.Model):
    ISBN = models.CharField(primary_key=True, max_length=30)
    Title = models.CharField(max_length=60)
    Author = models.CharField(max_length=60)
    NumOfPages = models.PositiveSmallIntegerField()
    Genre = models.CharField(max_length=120, default="")


class Connections(models.Model):
    User = models.CharField(max_length=60)
    Book = models.CharField(max_length=30)
