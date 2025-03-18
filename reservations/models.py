from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_hotel_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Room(models.Model):
    ROOM_TYPES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
    ]
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    capacity = models.IntegerField()
    amenities = models.TextField(default='[]')
    is_available = models.BooleanField(default=True)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"Room {self.number} - {self.type}"

    def main_image(self):
        main_img = self.images.filter(is_main=True).first()
        return main_img.image.url if main_img else None


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='room_images/')
    is_main = models.BooleanField(default=False)  # True si c'est l'image principale de la chambre

    def __str__(self):
        return f"Image for Room {self.room.number} ({'Main' if self.is_main else 'Secondary'})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Promotion(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return f"{self.code} - {self.discount}%"

    def is_active(self):
        """Vérifie si la promotion est actuellement valide"""
        from django.utils.timezone import now
        return self.valid_from <= now().date() <= self.valid_to
