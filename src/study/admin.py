from django.contrib import admin
from study.models import Study, Sample, Experiment, Run, Seq

# Register your models here.

#custome admin interface
class StudyAdmin(admin.ModelAdmin):
	list_display = ('name','desc','date_created', 'data_updated', 'owner')
	search_fields = ('name','owner',)
	readonly_fields=('date_created', 'data_updated')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Study)
admin.site.register(Sample)
admin.site.register(Experiment)
admin.site.register(Run)
admin.site.register(Seq)