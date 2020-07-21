from django import template

from ..models import (
    FacebookSocial,
    InstagramSocial,
    TwitterSocial,
    PinterestSocial,
    WhatsappSocial
)

register = template.Library()

@register.simple_tag
def get_handle(*args, **kwargs):
    social_media = kwargs['social_media']
    social_media = social_media.lower()
    if social_media == 'facebook':
        handle = FacebookSocial.objects.first()
    elif social_media == 'twitter':
        handle = TwitterSocial.objects.first()
    elif social_media == 'instagram':
        handle = InstagramSocial.objects.first()
    elif social_media == 'whatsapp':
        handle = WhatsappSocial.objects.first()
    elif social_media == 'pinterest':
        handle = PinterestSocial.objects.first()

    return handle.handle if handle else None