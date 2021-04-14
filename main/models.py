from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=300, blank=True)
    title2 = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title



class News(models.Model):
    title = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=300, blank=True)
    date = models.DateTimeField(blank=True)
    logo = models.ImageField(upload_to='upload')
    status = models.IntegerField(default=0, blank=True)
    rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
