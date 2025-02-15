from rest_framework import serializers
from .models import User, Room, Reservation, Review, Promotion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_hotel_staff', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True},  # Empêche le mot de passe d'être affiché dans les réponses
            'phone_number': {'required': False},  # Le champ phone_number est optionnel
            'is_hotel_staff': {'read_only': True},  # Non modifiable par l'utilisateur
            'is_admin': {'read_only': True},  # Non modifiable par l'utilisateur
        }

def create(self, validated_data):
    # Création d'un nouvel utilisateur en respectant les champs validés
    user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        phone_number=validated_data.get('phone_number', None),  # Gère les champs optionnels
    )
    user.set_password(validated_data['password'])  # Hash du mot de passe
    user.save()
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
