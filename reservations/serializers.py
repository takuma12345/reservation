from rest_framework import serializers
from .models import User, Room, Reservation, Review, Promotion, RoomImage
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_hotel_staff', 'is_admin', 'password']
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

from rest_framework import serializers
from .models import Room, RoomImage

class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'is_main', 'description']

class RoomSerializer(serializers.ModelSerializer):
    main_image_url = serializers.SerializerMethodField()  # Champ pour l'image principale
    images = RoomImageSerializer(many=True, read_only=True)  # Champ pour toutes les images

    class Meta:
        model = Room
        fields = [
            'id', 'type', 'price', 'description', 'capacity', 'amenities',
            'is_available', 'number', 'main_image_url', 'images'
        ]

    def get_main_image_url(self, obj):
        """
        Renvoie l'URL de l'image principale de la chambre.
        """
        return obj.main_image()





class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        """ Vérifie la disponibilité de la chambre avant de confirmer la réservation """
        check_in = data['check_in']
        check_out = data['check_out']
        room = data['room']

        if check_in >= check_out:
            raise ValidationError("La date d'arrivée doit être avant la date de départ.")

        # Vérifier si la chambre est déjà réservée à ces dates
        reservations = Reservation.objects.filter(
            room=room,
            check_out__gt=check_in,  # Si une réservation se termine après le check_in
            check_in__lt=check_out   # Et commence avant le check_out
        )

        if reservations.exists():
            raise ValidationError("Cette chambre est déjà réservée pour ces dates.")

        return data


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
