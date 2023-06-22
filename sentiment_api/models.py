# Create your models here.
from django.db import models


class Positive(models.Model):
    text=models.TextField()
    sentiment=models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.sentiment
    
class Negative(models.Model):
    text=models.TextField()
    sentiment=models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.sentiment
    
class Neutral(models.Model):
    text=models.TextField()
    sentiment=models.CharField(max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.sentiment