from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room  # Importez le modèle Room
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


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
