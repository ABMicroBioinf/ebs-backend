from django.contrib import admin
from .models import Sequence, SeqFile, MetadataFile
# Register your models here.


#custome admin interface
class SequenceAdmin(admin.ModelAdmin):
	list_display = [
        "id",
        "Experiment",
        "SampleName",
        "Projectid",
        "owner",
        "DateCreated"
    ]

admin.site.register(Sequence, SequenceAdmin)
admin.site.register(SeqFile)
admin.site.register(MetadataFile)

