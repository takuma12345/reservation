from django.contrib import admin

# Register your models here.

from .models import Room  # Importez le modèle Room
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import Reservation

from django.contrib import admin
from .models import RoomImage  # Importez le modèle RoomImage



class RoomAdmin(admin.ModelAdmin):
    list_display = ('type', 'price', 'capacity', 'is_available')  # Colonnes visibles dans l'admin
    search_fields = ('type', 'description')  # Champs de recherche
    list_filter = ('type', 'is_available')  # Filtres sur le côté droit

admin.site.register(Room, RoomAdmin)  # Enregistrez le modèle Room dans l'admin


class UserAdmin(BaseUserAdmin):
    # Champs affichés dans la liste des utilisateurs
    list_display = ('username', 'email', 'phone_number', 'is_hotel_staff', 'is_admin', 'is_active')
    list_filter = ('is_hotel_staff', 'is_admin', 'is_active')  # Filtres sur le côté droit

    # Champs éditables
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_hotel_staff', 'is_admin', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Champs utilisés pour créer un nouvel utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'is_hotel_staff', 'is_admin'),
        }),
    )

    search_fields = ('username', 'email', 'phone_number')  # Recherche
    ordering = ('username',)  # Ordre des utilisateurs
    filter_horizontal = ('groups', 'user_permissions')  # Permissions et groupes

# Enregistrer le modèle personnalisé User avec la configuration UserAdmin
admin.site.register(User, UserAdmin)




class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'total_price', 'is_paid', 'created_at')
    list_filter = ('user', 'room', 'is_paid')
    search_fields = ('user__username', 'room__name')

    def get_queryset(self, request):
        # Récupérer le queryset de base
        qs = super().get_queryset(request)

        # Si l'utilisateur est un superutilisateur, afficher toutes les réservations
        if request.user.is_superuser:
            return qs

        # Sinon, afficher uniquement les réservations de l'utilisateur connecté
        return qs.filter(user=request.user)

admin.site.register(Reservation, ReservationAdmin)

# Enregistrez le modèle RoomImage
@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room', 'image', 'is_main' ]  # Champs à afficher dans la liste
    list_editable = ['is_main']  # Permet de modifier 'is_main' directement depuis la liste
    list_filter = ['room', 'is_main']  # Filtres disponibles
    search_fields = ['room__number']  # Champs de recherche