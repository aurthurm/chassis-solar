from django.contrib import admin

from .models import (
    FacebookSocial,
    InstagramSocial,
    TwitterSocial,
    PinterestSocial,
    WhatsappSocial
)

admin.site.register(FacebookSocial)
admin.site.register(InstagramSocial)
admin.site.register(TwitterSocial)
admin.site.register(PinterestSocial)
admin.site.register(WhatsappSocial)