from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6 , decimal_places = 2)
    photo = models.ImageField(upload_to = 'photos/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default = True)
    publish_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['-publish_date']