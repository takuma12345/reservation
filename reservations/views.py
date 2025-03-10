from datetime import timezone

from rest_framework import viewsets, permissions

from . import serializers
from .models import User, Room, Reservation, Review, Promotion
from .serializers import UserSerializer, RoomSerializer, ReservationSerializer, ReviewSerializer, PromotionSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions
from .models import Reservation









class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        # Filtrer les chambres disponibles si l'action est 'list' ou 'retrieve'
        if self.action in ['list', 'retrieve']:
            return Room.objects.filter(is_available=True)
        return Room.objects.all()  # L'admin voit toutes les chambres

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]




class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [TokenAuthentication]  # Authentification par token
    permission_classes = [IsAuthenticated]  # Nécessite un utilisateur authentifié

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:  # Admin voit toutes les réservations
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)  # Filtre pour un utilisateur normal

    def perform_create(self, serializer):
        # Associer l'utilisateur actuel à la réservation lors de la création
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # S'assurer que l'utilisateur ne peut modifier que ses propres réservations
        if self.request.user.is_admin or serializer.instance.user == self.request.user:
            serializer.save()
        else:
            raise serializers.ValidationError("Vous ne pouvez modifier que vos propres réservations.")

    def perform_destroy(self, instance):
        # S'assurer que l'utilisateur ne peut supprimer que ses propres réservations
        if self.request.user.is_admin or instance.user == self.request.user:
            instance.delete()
        else:
            raise serializers.ValidationError("Vous ne pouvez supprimer que vos propres réservations.")


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Accès réservé aux utilisateurs authentifiés
    def get_queryset(self):
        """
        Filtre les promotions actives en fonction des paramètres.
        Par exemple, `?active=true` pour voir uniquement les promotions actives.
        """
        queryset = super().get_queryset()
        active = self.request.query_params.get('active')
        if active == 'true':
            queryset = queryset.filter(valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        return queryset



class RegisterView(APIView):
    """
    Vue publique pour enregistrer un nouvel utilisateur.
    """
    permission_classes = [AllowAny]  # Permet à tout le monde d'accéder à cet endpoint.

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))  # Hash le mot de passe.
            user.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "is_hotel_staff": user.is_hotel_staff,
                        "is_admin": user.is_admin
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    """
    Vue pour déconnecter un utilisateur en supprimant son jeton.
    """
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs connectés peuvent se déconnecter.

    def post(self, request, *args, **kwargs):
        try:
            # Récupérer le jeton de l'utilisateur connecté
            token = Token.objects.get(user=request.user)
            # Supprimer le jeton
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or user not logged in."}, status=status.HTTP_400_BAD_REQUEST)






class LoginView(APIView):
    """
    Vue pour gérer la connexion utilisateur.
    """
    permission_classes = [AllowAny]  # Permettre un accès public à cet endpoint.

    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        if not username_or_email or not password:
            return Response(
                {"error": "Username/Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Vérifier si l'utilisateur essaie de se connecter avec un email
            user = User.objects.get(email=username_or_email)
            username = user.username
        except User.DoesNotExist:
            # Sinon, essayer avec le nom d'utilisateur
            username = username_or_email

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Générer ou récupérer le jeton pour l'utilisateur
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_hotel_staff": user.is_hotel_staff,
                    "is_admin": user.is_admin
                }
            },
            status=status.HTTP_200_OK
        )
