from django.contrib import admin
from .models import Study, Run, SeqFile, MetadataFile
# Register your models here.


#custome admin interface
class StudyAdmin(admin.ModelAdmin):
	list_display = (
        "id",
        "title",
        "data_type",
        "date_created",
        "last_update",
        "owner",
    )

admin.site.register(Study, StudyAdmin)
admin.site.register(Run)
admin.site.register(SeqFile)
admin.site.register(MetadataFile)

