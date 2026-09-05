"""
Context Processors untuk Core App
"""
from .models import WebsiteSettings, ContactPerson, SocialMedia


def website_settings(request):
    """Context processor untuk WebsiteSettings - tersedia di semua template"""
    try:
        settings = WebsiteSettings.load()
    except Exception:
        settings = None
    
    try:
        contact_persons = ContactPerson.objects.filter(is_active=True)[:1]
    except Exception:
        contact_persons = []
    
    try:
        social_media = SocialMedia.objects.filter(is_active=True).order_by('order', 'platform')
    except Exception:
        social_media = []
    
    return {
        'settings': settings,
        'contact_persons': contact_persons,
        'social_media': social_media,
    }

