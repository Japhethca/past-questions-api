from django.urls import path
from django.views.generic import TemplateView

from .views import (
    index, login, signup, past_questions_details, logout, PastQuestionSearch
)


urlpatterns = [
    path('', index, name='home'),
    path(
        'about-us',
        TemplateView.as_view(template_name='web/pages/about.html'),
        name='about'
    ),
    path(
        'contact-us',
        TemplateView.as_view(template_name='web/pages/contact.html'),
        name='contact'
    ),
    path('accounts/login', login, name='login'),
    path('accounts/signup', signup, name='signup'),
    path('accounts/logout/', logout, name='logout'),
    path('past-questions', PastQuestionSearch.as_view(), name='past-question'),
    path('past-questions/<slug:pq_title>', past_questions_details, name='past-question'),
    path('search', PastQuestionSearch.as_view(), name='search')
]
