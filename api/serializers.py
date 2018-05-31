from rest_framework import serializers
from django.contrib.auth import get_user_model

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
