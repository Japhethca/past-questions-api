from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

RATINGS = (
    ('ONE', 1),
    ('TWO', 2),
    ('THREE', 3),
    ('FOUR', 4),
    ('FIVE', 5)
)


class School(models.Model):
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class PastQuestion(models.Model):
    subject_name = models.CharField(max_length=300)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject_name}'


class Review(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    past_question = models.ForeignKey(PastQuestion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment}'


class History(models.Model):
    past_question = models.ForeignKey(PastQuestion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.past_question}'


class Rating(models.Model):
    rate = models.IntegerField(choices=RATINGS)
    past_question = models.ForeignKey(PastQuestion, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rate}'
