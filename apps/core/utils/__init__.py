from django.conf import settings
from django.contrib.sites.models import Site
import logging
import socket
from typing import TYPE_CHECKING, Optional, Type, Union
from urllib.parse import urljoin
from django.db.models import Model
from django.utils.encoding import iri_to_uri
from django.utils.text import slugify


def choose_existing(wanted, alternative):
    return wanted if wanted else alternative


def build_absolute_uri(location: str) -> Optional[str]:
    host = Site.objects.get_current().domain
    protocol = "https" if settings.ENABLE_SSL else "http"
    current_uri = "%s://%s" % (protocol, host)
    location = urljoin(current_uri, location)
    return iri_to_uri(location)
