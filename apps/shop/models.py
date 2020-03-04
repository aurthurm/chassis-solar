from typing import TYPE_CHECKING, Iterable, Optional, Union
from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from versatileimagefield.fields import PPOIField, VersatileImageField

from apps.core.models import (
    SeoModel,
    PublishableModel,
    PublishedQuerySet,
)

from apps.core.utils import build_absolute_uri


class Category(MPTTModel, SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = VersatileImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    minimun_price_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    objects = models.Manager()
    tree = TreeManager()

    def __str__(self) -> str:
        return self.name


class Brand(SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    background_image = VersatileImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    has_variants = models.BooleanField(default=False)
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    weight = models.CharField(max_length=20)

    class Meta:
        app_label = "shop"

    def __str__(self) -> str:
        return self.name


class Product(SeoModel, PublishableModel):
    product_type = models.ForeignKey(
        ProductType, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    price_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = VersatileImageField(upload_to="products", ppoi_field="ppoi", blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    def get_ordering_queryset(self):
        return self.product.images.all
    
    def __str__(self):
        return self.product.name + " <image alt:> " +self.alt


class ProductVariant(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    price_override_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    images = models.ManyToManyField(ProductImage, through="VariantImage")
    track_inventory = models.BooleanField(default=True)

    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "shop"

    def __str__(self) -> str:
        return self.name or self.sku

    @property
    def is_visible(self) -> bool:
        return self.product.is_visible

    def get_weight(self):
        return self.weight or self.product.weight or self.product.product_type.weight

    def is_shipping_required(self) -> bool:
        return self.product.product_type.is_shipping_required

    def get_first_image(self) -> "ProductImage":
        images = list(self.images.all())
        return images[0] if images else self.product.get_first_image()

    def get_absolute_url(self):
        return reverse('shop:variant-detail', kwargs={'product_variant_id': self.pk})

    def get_product_url(self):
        return reverse('shop:product-detail', kwargs={'product_variant_id': self.pk})


class VariantImage(models.Model):
    variant = models.ForeignKey(
        ProductVariant, related_name="variant_images", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        ProductImage, related_name="variant_images", on_delete=models.CASCADE
    )
    
    def __str__(self):
        return "<variant:> " + self.variant.name + " <image alt:> " + self.image.alt


class CollectionProduct(models.Model):
    collection = models.ForeignKey(
        "Collection", related_name="collectionproduct", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="collectionproduct", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("collection", "product"),)

    def get_ordering_queryset(self):
        return self.product.collectionproduct.all()


class Collection(SeoModel, PublishableModel):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="collections",
        through=CollectionProduct,
        through_fields=("collection", "product"),
    )
    background_image = VersatileImageField(
        upload_to="collection-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.name



class DigitalContent(models.Model):
    FILE = "file"
    TYPE_CHOICES = ((FILE, "digital_product"),)
    automatic_fulfillment = models.BooleanField(default=True)
    content_type = models.CharField(max_length=128, default=FILE, choices=TYPE_CHOICES)
    product_variant = models.OneToOneField(
        ProductVariant, related_name="digital_content", on_delete=models.CASCADE
    )
    content_file = models.FileField(upload_to="digital_contents", blank=True)
    max_downloads = models.IntegerField(blank=True, null=True)
    url_valid_days = models.IntegerField(blank=True, null=True)

    def create_new_url(self) -> "DigitalContentUrl":
        return self.urls.create()

    def __str__(self):
        return self.product_variant.name


class DigitalContentUrl(models.Model):
    token = models.UUIDField(editable=False, unique=True)
    content = models.ForeignKey(
        DigitalContent, related_name="urls", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    download_num = models.IntegerField(default=0)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.token:
            self.token = str(uuid4()).replace("-", "")
        super().save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self) -> Optional[str]:
        url = reverse("digital-product", kwargs={"token": str(self.token)})
        return build_absolute_uri(url)