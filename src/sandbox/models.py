from djongo import models
from django import forms
from django.conf import settings
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            'name', 'tagline'
        )

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    class Meta:
        abstract = True

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            'name', 'email'
        )

class Reference(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
            return self.name
   

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = (
            'name', 'url'
        )
    def __str__(self):
            return self.name


class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog,
        model_form_class=BlogForm
    )
    
    headline = models.CharField(max_length=255)    
    authors = models.ArrayField(
        model_container=Author,
        model_form_class=AuthorForm
    )
    """ reference = models.ForeignKey(
        'Reference', related_name = 'entries', on_delete=models.CASCADE)
     """
    """ references = models.ArrayReferenceField(
        to=Reference,
        on_delete=models.CASCADE,
    ) """

    reference = models.ForeignKey(Reference, related_name="sandbox_refers", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sandbox_owners", on_delete=models.CASCADE)

    objects = models.DjongoManager()

    def __str__(self):
        return self.headline