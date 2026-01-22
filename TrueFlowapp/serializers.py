from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True) # Confirm Password

    class Meta:
        model = CustomUser
        fields = ['username', 'email','phone_number', 'password','confirm_password']
        # fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return data

    def create(self, validated_data):
        # Remove password2 before creating user
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            userObj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=userObj.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data
