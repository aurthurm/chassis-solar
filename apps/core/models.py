from django.db import models
from django.core.validators import MaxLengthValidator
import datetime
from django.db import models

class PublishedQuerySet(models.QuerySet):
    def published(self):
        today = datetime.date.today()
        return self.filter(
            Q(publication_date__lte=today) | Q(publication_date__isnull=True),
            is_published=True,
        )

    @staticmethod
    def user_has_access_to_all(user):
        return user.is_active

    def visible_to_user(self, user):
        if self.user_has_access_to_all(user):
            return self.all()
        return self.published()


class SeoModel(models.Model):
    seo_title = models.CharField(
        max_length=70, blank=True, null=True, validators=[MaxLengthValidator(70)]
    )
    seo_description = models.CharField(
        max_length=300, blank=True, null=True, validators=[MaxLengthValidator(300)]
    )

    class Meta:
        abstract = True

class PublishableModel(models.Model):
    publication_date = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def is_visible(self):
        return self.is_published and (
            self.publication_date is None
            or self.publication_date < datetime.date.today()
        )
