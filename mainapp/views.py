import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory

links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    products = Product.objects.all()[:4]
    context = {
        'title': 'Главная',
        'products': products,
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'products': product_paginator,
            'category': category,
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукты'
    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):
    json_data = json.loads(open('mainapp/contacts_data.json').read())
    context = {
        'title': 'Контакты',
        'phone': 'Телефон',
        'email': 'Email',
        'address': 'Адрес',
        'contacts': json_data,
    }

    return render(request, 'mainapp/contact.html', context)

