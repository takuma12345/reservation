from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Room, User, Review  # Importez les modèles Room et User

from .models import Reservation


# Configuration pour le modèle Room
class RoomAdmin(admin.ModelAdmin):
    list_display = ('type', 'price', 'capacity', 'is_available')  # Colonnes visibles dans l'admin
    search_fields = ('type', 'description')  # Champs de recherche
    list_filter = ('type', 'is_available')  # Filtres sur le côté droit

# Enregistrez le modèle Room dans l'admin
admin.site.register(Room, RoomAdmin)

# Configuration pour le modèle User
class CustomUserAdmin(BaseUserAdmin):
    # Champs affichés dans la liste des utilisateurs
    list_display = ('username', 'email', 'phone_number', 'is_hotel_staff', 'is_admin', 'is_active', 'date_joined')
    list_filter = ('is_hotel_staff', 'is_admin', 'is_active')  # Filtres sur le côté droit

    # Champs éditables dans le formulaire d'édition
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
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_hotel_staff', 'is_admin', 'is_active'),
        }),
    )

    search_fields = ('username', 'email', 'phone_number')  # Recherche
    ordering = ('username',)  # Ordre des utilisateurs
    filter_horizontal = ('groups', 'user_permissions')  # Permissions et groupes

# Enregistrez le modèle User avec la configuration CustomUserAdmin
admin.site.register(User, CustomUserAdmin)



# Configuration pour le modèle Reservation


class ReservationAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface admin pour le modèle Reservation.
    """
    list_display = ('user', 'room', 'check_in', 'check_out', 'total_price', 'is_paid', 'created_at')  # Colonnes affichées
    list_filter = ('is_paid', 'created_at', 'check_in', 'check_out')  # Ajout de filtres sur les dates de séjour
    search_fields = ('user__username', 'room__type')  # Recherche par nom d'utilisateur ou type de chambre
    ordering = ('-created_at',)  # Trier par date de création, du plus récent au plus ancien
    date_hierarchy = 'created_at'  # Ajout d'une navigation par date en haut de la liste

# Enregistrer le modèle avec cette configuration
admin.site.register(Reservation, ReservationAdmin)




class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'rating', 'comment', 'created_at')  # Colonnes visibles
    list_filter = ('rating', 'created_at')  # Filtres sur le côté
    search_fields = ('user__username', 'room__id', 'comment')  # Barre de recherche
    ordering = ('-created_at',)  # Ordre par défaut
    readonly_fields = ('created_at',)  # Champs non modifiables

admin.site.register(Review, ReviewAdmin)

