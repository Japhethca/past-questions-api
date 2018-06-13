from django.contrib import admin
from .models import (
    User, PastQuestion, School, History, Review, Subject, Rating
)
# Register your models here.


class PastQuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.site_header = 'Past QA Admin'
admin.site.site_title = 'Past QA'
admin.site.index_title = 'Past QA Administration'
admin.site.register(User)
admin.site.register(PastQuestion, PastQuestionAdmin)
admin.site.register(School)
admin.site.register(History)
admin.site.register(Review)
admin.site.register(Subject)
admin.site.register(Rating)
