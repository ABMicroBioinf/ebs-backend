from djongo import models

class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    street_line_1 = models.CharField(max_length=255)
    street_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=10)
    slug = models.SlugField(blank=True, unique=True)

    #avatar = models.FileField(upload_to='sandbox/', verbose_name="Head portrait", null=True)
    def __str__(self):
        return self.name