from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class LoginHistory(models.Model):
    """Model untuk tracking login history (berhasil dan gagal)"""
    STATUS_CHOICES = [
        ('success', 'Berhasil'),
        ('failed', 'Gagal'),
    ]
    
    username = models.CharField(max_length=150, verbose_name='Username')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP Address')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Status')
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='login_history',
        verbose_name='User'
    )
    error_message = models.CharField(max_length=255, blank=True, verbose_name='Pesan Error')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')
    
    class Meta:
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.get_status_display()} - {self.created_at}"


class User(AbstractUser):
    """Custom User Model untuk Admin dan Panitia"""
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('bendahara', 'Bendahara'),
        ('petugaspendaftaran', 'Petugas Pendaftaran'),
        ('user', 'User Biasa'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='petugaspendaftaran',
        verbose_name='Role'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='No. HP')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True, verbose_name='Foto Profil')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin_user(self):
        """Check if user is superadmin or Django superuser"""
        return self.role == 'superadmin' or self.is_superuser
    
    def is_bendahara(self):
        """Check if user is bendahara"""
        return self.role == 'bendahara' or self.is_admin_user()
    
    def is_petugas_pendaftaran(self):
        """Check if user is petugas pendaftaran"""
        return self.role == 'petugaspendaftaran' or self.is_admin_user()
