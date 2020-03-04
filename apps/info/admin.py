from django.contrib import admin

from .models import (
    HomeInfo,
    About,
    Contact,
    Member,
    OtherContacts
)

admin.site.register(HomeInfo)
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(Member)
admin.site.register(OtherContacts)