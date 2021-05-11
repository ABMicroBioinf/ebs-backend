from rest_framework import serializers

from study.models import Study, Sample, Experiment, Run, Seq


class CreateStudySerializer(serializers.ModelSerializer):
    '''
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
    '''

    class Meta:
        model = Study
        fields = ['title', "description"]

    def save(self):
        pass


class DetailStudySerializer(serializers.ModelSerializer):
    '''
        context = {}

        study = get_object_or_404(Study, slug=slug)
        context['study'] = study

        return render(request, 'study/detail_study.html', context)
    '''

    class Meta:
        model = Study
        fields = '__all__'

    def save(self):
        pass


class EditStudySerializer(serializers.ModelSerializer):
    '''
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
    '''

    class Meta:
        model = Study
        fields = '__all__'

    def save(self):
        pass
