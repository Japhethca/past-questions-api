from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.search import SearchVector

from web.helpers import to_str
from .forms import (
    LoginForm, SignupForm, ReviewForm
)
from core.models import PastQuestion, Review, User, School, Subject


def index(request):
    past_questions = PastQuestion.objects.all()[:6]
    return render(request, 'web/pages/home.html', {'past_questions': past_questions})


def login(request):
    login_error = []

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                user = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                user = None

            if user is not None and check_password(request.POST.get('password'), user.password):
                auth_login(request, user)
                if request.path == request.previous_url:
                    return redirect('home')
                return redirect(request.previous_url)
            else:
                login_error.append("Invalid Credential, either email or password is not correct")
    else:
        login_form = LoginForm()
    return render(
        request,
        'web/pages/login.html',
        context={'form': login_form, 'login_error': login_error}
    )


def signup(request):

    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            print(signup_form.cleaned_data)
            user = User.objects.create_user(**signup_form.cleaned_data)
            login(request, user)

    else:
        signup_form = SignupForm()
    return render(request, 'web/pages/signup.html', context={'form': signup_form})


def past_questions_details(request, pq_title=None):
    pq_title = pq_title
    past_question = get_object_or_404(PastQuestion, slug=pq_title)
    pq_reviews = Review.objects.filter(past_question__slug=pq_title)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            pq_reviews.create(
                comment=review_form.cleaned_data.get('comment'),
                past_question_id=past_question.id,
                user=request.user
            )
            review_form = ReviewForm()
    else:
        review_form = ReviewForm()
    return render(request, 'web/pages/pq-single.html', context={
        'pq': past_question,
        'pq_reviews': pq_reviews,
        'review_form': review_form
    })


def logout(request):
    auth_logout(request)

    if request.path == request.previous_url:
        return redirect('home')
    return redirect(request.previous_url)


class PastQuestionSearch(ListView):
    model = PastQuestion
    queryset = PastQuestion.objects.all()
    ordering = ['title']
    http_method_names = ['get']
    template_name = {
        'search': 'web/pages/search.html',
        'past-question': 'web/pages/past-questions.html'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.school_name = ''
        self.subject_name = ''

    def get_queryset(self):
        queryset = self.queryset
        search_query = self.request.GET.get('q', '')
        self.school_name = to_str(self.request.GET.get('school', ''))
        self.subject_name = to_str(self.request.GET.get('subject', ''))
        result = []

        if self.school_name and self.subject_name:
            result = queryset.filter(
                school__name__icontains=self.school_name,
                subjects__name__icontains=self.subject_name
            )

        elif self.subject_name:
            result = queryset.filter(subjects__name__icontains=self.subject_name)

        elif self.school_name:
            result = queryset.filter(school__name__icontains=self.school_name)

        elif search_query:
            result = queryset.annotate(
                search=SearchVector(
                    'title', 'school__name', 'school__shortname',
                    'description', 'subjects__name')
            ).filter(search=search_query)
        else:
            return queryset

        return result.distinct('title')

    def get_template_names(self):
        template_type = self.request.GET.get('q', None)

        if template_type is not None:
            return [self.template_name.get('search')]
        else:
            return self.template_name.get('past-question')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.school_name:
            try:
                context['query_title'] = School.objects.filter(
                    name__icontains=self.school_name).first().name
            except School.DoesNotExist:
                context['query_title'] = None

        if self.subject_name:
            try:
                context['query_title'] = Subject.objects.filter(
                    name__icontains=self.subject_name).first().name
            except Subject.DoesNotExist:
                context['query_title'] = None

        return context




