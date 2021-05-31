from djongo import models

import os
_roles_path = "company"
 
 
def var_dir(instance, filename):
    return os.path.join(_roles_path, instance.id, 'vars', filename)
 
 
def task_dir(instance, filename):
    return os.path.join(_roles_path, instance.id, 'tasks', filename)
 

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
   
    #directory = models.FilePathField(path=_roles_path, match='*.yml', recursive=True, max_length=200)
    tasks = models.FileField(upload_to=task_dir, blank=False)
    vars = models.FileField(upload_to=var_dir)

    def __str__(self):
        return self.name

