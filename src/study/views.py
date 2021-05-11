from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from study.models import Study
from study.forms import CreateStudyForm, UpdateStudyForm
from account.models import Account


def create_study_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateStudyForm(request.POST or None)
	if form.is_valid():
		obj = form.save(commit=False)
		account = Account.objects.filter(email=user.email).first()
		obj.owner = account
		obj.save()
		form = CreateStudyForm()

	context['form'] = form

	return render(request, "study/create_study.html", context)


def detail_study_view(request, slug):

	context = {}

	study = get_object_or_404(Study, slug=slug)
	context['study'] = study

	return render(request, 'study/detail_study.html', context)



def edit_study_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	study = get_object_or_404(Study, slug=slug)

	if study.owner != user:
		return HttpResponse('You are not the owner of that study.')

	if request.POST:
		form = UpdateStudyForm(request.POST or None, instance=study)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			study = obj

	form = UpdateStudyForm(
			initial = {
					"title": study.study_title,
					"body": study.study_summary,
			}
		)

	context['form'] = form
	return render(request, 'study/edit_study.html', context)
