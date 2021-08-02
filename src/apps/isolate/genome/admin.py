
# Register your models here.
from django.contrib import admin
from .models import Genome, Annotation

# Register your models here.
class GenomeAdmin(admin.ModelAdmin):
    """ list_display = (
        "name",
        "main_lin",
        "sublin",
        "drtype",
        "num_dr_variants",
        "num_other_variants"
    ) """
class AnnotationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genome, GenomeAdmin)
admin.site.register(Annotation, AnnotationAdmin)