from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Room, Reservation, Review, Promotion
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_hotel_staff', 'is_admin']

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                phone_number=validated_data.get('phone_number', ''),
                password=validated_data['password']
            )
            return user

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['id', 'code', 'discount', 'valid_from', 'valid_to', 'is_active']

    def get_is_active(self, obj):
        """Retourne si la promotion est valide"""
        return obj.is_active()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            return data
        raise serializers.ValidationError("Email and password are required.")
