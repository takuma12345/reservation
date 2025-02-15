from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoomViewSet, ReservationViewSet, ReviewViewSet, PromotionViewSet, RegisterView, \
    LoginView, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'promotions', PromotionViewSet, basename='promotion')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),  # Route pour l'inscription
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
