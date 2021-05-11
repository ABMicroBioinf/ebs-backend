from django import forms

from study.models import Study, Sample, Experiment, Run, Seq


class CreateStudyForm(forms.ModelForm):

	class Meta:
		model = Study
		fields = ['title', "description"]


class UpdateStudyForm(forms.ModelForm):

	class Meta:
		model = Study
		fields = ['title', 'description']

	def save(self, commit=True):
		study = self.instance
		study.title = self.cleaned_data['title']
		study.description = self.cleaned_data['description']

		if commit:
			study.save()
		return study


class CreateSampleForm(forms.ModelForm):

	class Meta:
		model = Sample
		fields = ['title', 'taxon_id',
                    'scientific_name', 'common_name', 'description']


class UpdateSampleForm(forms.ModelForm):

	class Meta:
		model = Sample
		fields = ['title', 'taxon_id',
                    'scientific_name', 'common_name', 'description']


	def save(self, commit=True):
		sample = self.instance
		sample.title = self.cleaned_data['title']
		sample.taxon_id = self.cleaned_data['taxon_id']
		sample.scientific_name = self.cleaned_data['scientific_name']
		sample.common_name = self.cleaned_data['common_name']
		sample.description = self.cleaned_data['description']

		if commit:
			sample.save()
		return sample


class CreateExperimentForm(forms.ModelForm):

	class Meta:
		model = Experiment
		fields = ['title', 'library_name', 'platform', 'instrument_model',
                    'library_strategy', 'library_source', 'library_layout', 'library_selection']


class UpdateExperimentForm(forms.ModelForm):

	class Meta:
		model = Experiment
		fields = ['title', 'library_name', 'platform', 'instrument_model',
                    'library_strategy', 'library_source', 'library_layout', 'library_selection']

	def save(self, commit=True):
		experiment = self.instance
		experiment.title = self.cleaned_data['title']
		experiment.instrument_model = self.cleaned_data['instrument_model']
		experiment.library_strategy = self.cleaned_data['library_strategy']
		experiment.library_source = self.cleaned_data['library_source']
		experiment.library_layout = self.cleaned_data['library_layout']
		experiment.library_selection = self.cleaned_data['library_selection']

		if commit:
			experiment.save()
		return experiment

class CreateRunForm(forms.ModelForm):

	class Meta:
		model = Run
		fields = ['name', 'date_run']
	
class UpdateRunForm(forms.ModelForm):
	"""
	forms.DateTimeField(input_formats=['%m/%d/%y'],
       widget = forms.DateTimeInput(
          format ='%m/%d/%y',
          attrs=  {'class':'form-control'}))
	"""
	class Meta:
		model = Run
		fields = ['name', 'date_run']
	
	def save(self, commit=True):
		run = self.instance
		run.name = self.cleaned_data['name']
		run.date_run = self.cleaned_data['date_run']

		if commit:
			run.save()
		return run

class CreateSeqFrom(forms.ModelForm):

	class Meta:
		model = Seq
		fields = ['seqfile', 'avg_length', 'bases', 'count']

class UpdateSeqFrom(forms.ModelForm):

	class Meta:
		model = Seq
		fields = ['seqfile', 'avg_length', 'bases', 'count']

	def save(self, commit=True):
		seq = self.instance
		seq.avg_length = self.cleaned_data['avg_length']
		seq.bases = self.cleaned_data['bases']
		seq.count = self.cleaned_data['count']
		seq.seqfile = self.cleaned_data['seqfile']

		if commit:
				seq.save()
		return seq
