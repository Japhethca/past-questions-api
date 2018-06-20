from core.models import PastQuestion, School, Subject


def sidebar_context(request):
    latest_pastquestions = PastQuestion.objects.all().order_by('created_at')[:6]
    schools = School.objects.all().order_by('name')[:6]
    subjects = Subject.objects.all().order_by('name')[:6]

    return {
        'latest_pastquestions': latest_pastquestions,
        'schools': schools,
        'subjects': subjects
    }
