from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models.past_question import (
    PastQuestion, School, Rating, Review, History
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, **kwargs):
        user = self.Meta.model
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')

        if email and password:
            user = self.Meta.model.objects.create_user(email, password=password)
            user.first_name = self.validated_data.get('first_name')
            user.last_name = self.validated_data.get('last_name')
            user.is_active = True
            user.save(**kwargs)
        return user


class PastQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastQuestion
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
