from rest_framework import viewsets, permissions
from .models import User, Room, Reservation, Review, Promotion
from rest_framework import generics, permissions
from .serializers import UserSerializer, RoomSerializer, ReservationSerializer, ReviewSerializer, PromotionSerializer, \
    LoginSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAdminUser]  # Seul l'admin peut accéder à ces vues

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

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
    from rest_framework import generics, permissions


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Autoriser tout le monde à s'inscrire

    from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
        return Response(serializer.errors, status=400)