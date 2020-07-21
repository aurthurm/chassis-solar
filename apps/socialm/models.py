from django.db import models

class SocialBase(models.Model):
    name = models.CharField(
        max_length=100
    )
    handle = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name + " - handle/username: " + self.handle

    class Meta:
        abstract = True


class FacebookSocial(SocialBase):
    pass


class TwitterSocial(SocialBase):
    pass


class InstagramSocial(SocialBase):
    pass


class PinterestSocial(SocialBase):
    pass


class WhatsappSocial(SocialBase):
    pass