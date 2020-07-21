from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField
from apps.shop.models import DigitalContent



class BaseInfo(models.Model):
    heading = models.CharField(
        max_length=100
    )
    message = models.TextField()

    class Meta:
        abstract = True


class HomeInfo(BaseInfo):
    """
    eg: heading: Welcome to ......
        message: We are experts .....
        outro: What we are known for is ...
    """
    categories_heading = models.CharField(
        max_length=100
    )
    outro = models.TextField()

    def __str__(self):
        return self.heading


class Member(BaseInfo):
    """
    eg: heading: Director
        message: Qualifications etc
    """
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    image = VersatileImageField(
        upload_to="products",
        blank=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name


class Contact(BaseInfo):
    """
    eg: heading: Gweru
        message: Cnr 4th and JMN Ave first floor office 5
    """

    def __str__(self):
        return self.heading
    
class OtherContacts(BaseInfo):
    message = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.heading


class About(BaseInfo):
    """
    eg: heading: About
        message: About message ....
    """
    team = models.ManyToManyField(
        "Member",
        blank=True
    )
    contacts = models.ManyToManyField(
        "Contact",
        blank=True
    )
    downloads = models.ManyToManyField(
        DigitalContent,
        blank=True
    )
    other_refs = models.ManyToManyField(
        OtherContacts,
        blank=True
    )

    def __str__(self):
        return self.heading

