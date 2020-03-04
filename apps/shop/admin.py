from django.contrib import admin
from .models import (
    Category,
    Brand,
    ProductType,
    Product,
    ProductImage,
    ProductVariant,
    VariantImage,
    CollectionProduct,
    Collection,
    DigitalContent,
    DigitalContentUrl
)


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(VariantImage)
admin.site.register(ProductVariant)
admin.site.register(CollectionProduct)
admin.site.register(Collection)
admin.site.register(DigitalContent)
admin.site.register(DigitalContentUrl)