
# Register your models here.
from django.contrib import admin
from .models import Assembly, Annotation, Mlst

# Register your models here.
class AssemblyAdmin(admin.ModelAdmin):
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

class MlstAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'st',
        'scheme',
        'owner'
        
    )
admin.site.register(Assembly, AssemblyAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Mlst, MlstAdmin)