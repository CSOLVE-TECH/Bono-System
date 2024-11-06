from rest_framework import serializers
from .models import Bonos,GeneratedBono, User
import secrets
import string
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings


#UserSerializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'password', 'phone', 'gender', 'is_superadmin', 'is_admin', 'is_user', 'is_deleted', 'status', 'deleted_by', 
            'added_by', 'status_changed_by', 'created_at','photo'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False}  # Removing read_only and using required=False
        }

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        password = validated_data.pop('password', None)

        # Set username to email automatically
        validated_data['username'] = phone
        validated_data['phone'] = phone

        user = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(8))
            user.set_password(password)  
        print(phone,password)
        user.save()
        print('mmmmmmmmmmmmm',user)
        # create chatting room at the user creation

        return user
    
# Bono Serializer
class BonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonos
        fields = '__all__'

# GeneratedBono Serializer
class GeneratedBonoSerializer(serializers.ModelSerializer):
    khat_owner_name = serializers.CharField(source='bono.khat_owner_name', read_only=True)
    khat_type = serializers.CharField(source='bono.khat_type', read_only=True)
    count = serializers.IntegerField(source='bono.count', read_only=True)

    class Meta:
        model = GeneratedBono
        fields = ['id', 'bono', 'khat_owner_name', 'khat_type', 'count', 'price', 'trader_signature', 'added_by']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # Validate username and password
        data = super().validate(attrs)
        user = self.user

        # Custom condition: Check if the user is active and not deleted
        if not user.is_active or user.is_deleted:
            raise serializers.ValidationError("User account is inactive or has been deleted.")

        # Optionally, update the last login time
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        # Return tokens in the response
        data['refresh'] = str(self.get_token(user))
        data['access'] = str(self.get_token(user).access_token)

        return data
