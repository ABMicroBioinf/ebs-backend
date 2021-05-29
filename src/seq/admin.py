from django.contrib import admin
from seq.models import Study, Run, SeqFile, MetadataFile
# Register your models here.

admin.site.register(Study)
admin.site.register(Run)
admin.site.register(SeqFile)
admin.site.register(MetadataFile)
