from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db.models import Q, F, Prefetch, Sum
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import json, math

from .models import (
    Category,
    Brand,
    ProductVariant
)
from ..info.models import HomeInfo

class HomeView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'home.html'

    def get_queryset(self):
        results = super(HomeView, self).get_queryset()
        results = results.filter().distinct()
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        home_info = HomeInfo.objects.first()
        context['heading'] = home_info.heading
        context['message'] = home_info.message
        context['cat_heading'] = home_info.categories_heading
        context['outro'] = home_info.outro
        return context


class ShopView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context['categories'] = categories
        context['brands'] = brands
        return context
    
class ProductsList(ListView):

    def get(self, *args, **kwargs):
        context = {}
        brands = []
        products = []
        categories = []

        _brands = Brand.objects.all()
        for b in _brands:
            brand = {
                'id': b.id,
                'name': b.name
            }
            brands.append(brand)

        _categories = Category.objects.all()
        for c in _categories:
            category = {
                'id': c.id,
                'name': c.name
            }
            categories.append(category)

        filter_category = self.request.GET.get('category', None)
        filter_brands = self.request.GET.getlist('brands[]')
        search =  self.request.GET.get('search', None)
        page = self.request.GET.get('page', 1)

        product_variants = ProductVariant.objects.all()

        if filter_brands:
            product_variants = product_variants.filter(
                product__brand__name__in=filter_brands
            )

        if filter_category:
            product_variants = product_variants.filter(
                product__category__name__iexact=filter_category
            )
        
        if search:
            product_variants = product_variants.filter(
                Q(name__icontains = search) |
                Q(description__icontains = search) |
                Q(sku__icontains = search) |
                Q(product__category__name__icontains = search) |
                Q(product__brand__name__icontains = search) |
                Q(product__name__icontains = search) |
                Q(product__description__icontains = search) |
                Q(product__slug__icontains = search) |
                Q(product__product_type__name__icontains = search) |
                Q(product__product_type__slug__icontains = search)
            )

        product_variants = product_variants.distinct()

        number_of_products = len(product_variants)
        paginate_by = 10
        number_of_pages = number_of_products/paginate_by
        
        paginator = Paginator(product_variants, paginate_by)

        try:
            paged_products = paginator.page(page)
        except PageNotAnInteger:
            paged_products = paginator.page(1)
        except EmptyPage:
            paged_products = paginator.page(paginator.num_pages)

        for variant in paged_products:
            images = [image.image.url for image in variant.images.all()]
            product = {
                'id': variant.pk,
                'sku': variant.sku,
                'name': variant.name,
                'product_id': variant.product.pk,
                'variant_url': variant.get_product_url(),
                'price': variant.price_override_amount if variant.price_override_amount else variant.product.price_amount ,
                'image1': images[0] if len(images) > 0 else '',
                'image2': images[1] if len(images) > 1 else ''
            }
            products.append(product)

        context['categories'] = categories
        context['brands'] =  brands
        context['products'] =  products
        context['pages'] = list(range(1, math.ceil(number_of_pages) + 1))
        return JsonResponse(context)


class ProductDetailView(TemplateView):
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        brands = Brand.objects.all()
        variant = get_object_or_404(ProductVariant, pk=kwargs['product_variant_id'])
        images = [img.image.url for img in variant.images.all()]
        context['name'] = variant.name
        context['sku'] = variant.sku
        context['price'] = variant.price_override_amount  if variant.price_override_amount else variant.product.price_amount ,
        context['old_price'] = variant.old_price      
        context['product_id'] = variant.product.id      
        context['description'] = variant.description  if variant.description.strip() != '' else variant.product.description
        context['images0'] = variant.get_first_image().image.url  
        context['images1'] = images[1] if len(images) > 1 else ''
        context['images2'] = images[2] if len(images) > 2 else ''
        context['images3'] = images[3] if len(images) > 3 else ''
        context['images4'] = images[4] if len(images) > 4 else ''
        context['images'] = images
        context['categories'] = categories
        context['brands'] = brands
        context['product_url'] = variant.get_absolute_url
        return context


class VariantDetail(View):
    """
    Same as ProductDetailView
    but this is called using ajax
    """
	
    def get(self, *args, **kwargs):
        representation= {}
        variant = get_object_or_404(ProductVariant, pk=kwargs['product_variant_id'])
        images = [img.image.url for img in variant.images.all()]
        representation['name'] = variant.name
        representation['sku'] = variant.sku
        representation['price'] =  variant.price_override_amount  if variant.price_override_amount else variant.product.price_amount
        representation['old_price'] = variant.old_price        
        representation['product_id'] = variant.product.id   
        representation['images0'] = variant.get_first_image().image.url  
        representation['images1'] = images[1] if len(images) > 1 else ''
        representation['images2'] = images[2] if len(images) > 2 else ''
        representation['images3'] = images[3] if len(images) > 3 else ''
        representation['images4'] = images[4] if len(images) > 4 else ''
        representation['images'] = images
        return JsonResponse(representation)

        "background-image: url(" +  + ");"