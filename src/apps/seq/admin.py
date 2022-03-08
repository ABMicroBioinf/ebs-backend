from django.contrib import admin
from .models import Sequence, SeqFile, MetadataFile, Project
# Register your models here.


#custome admin interface
class SequenceAdmin(admin.ModelAdmin):
	list_display = [
        "id",
        "Experiment",
        "project",
        "owner",
     
        "DateCreated"
    ]

admin.site.register(Sequence, SequenceAdmin)
admin.site.register(SeqFile)
admin.site.register(MetadataFile)
admin.site.register(Project)

