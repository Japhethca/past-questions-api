from django.db import models

from django.utils.text import slugify
from django.contrib.auth import get_user_model

from .base import BaseModel

User = get_user_model()

RATINGS = (
    ('ONE', 1),
    ('TWO', 2),
    ('THREE', 3),
    ('FOUR', 4),
    ('FIVE', 5)
)


class School(BaseModel):
    name = models.CharField(max_length=300)
    shortname = models.CharField(max_length=20, default=' ')
    logo_url = models.URLField(default='', null=True)

    def __str__(self):
        return f'{self.name}'


class Subject(BaseModel):
    name = models.CharField(max_length=300)
    shortname = models.CharField(max_length=5, blank=True, null=True)

    def save(self, *args, **kwargs):
        if 'shortname' not in kwargs.keys():
            if len(self.name.split(' ')) > 1:
                self.shortname = ''.join([name[0] for name in self.name.split(' ')])
            else:
                self.shortname = self.name[:4]
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class PastQuestion(BaseModel):
    title = models.CharField(max_length=300, db_index=True)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_index=True)
    description = models.TextField(default=None, null=True)
    download_url = models.URLField(default=None, null=True)
    subjects = models.ManyToManyField(Subject, default=None)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    cover_photo = models.URLField(default=' ')
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Review(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    past_question = models.ForeignKey(PastQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.comment}'


class History(BaseModel):
    past_question = models.ForeignKey(PastQuestion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Histories'

    def __str__(self):
        return f'{self.user}: {self.past_question}'


class Rating(BaseModel):
    rate = models.IntegerField(choices=RATINGS)
    past_question = models.ForeignKey(PastQuestion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rate}'
