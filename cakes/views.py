from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from cakes.models import Category, Product


class MainPageView(TemplateView):
    template_name = 'main.html'


class CategoryView(ListView):
    template_name = 'category_list.html'
    model = Category


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        obj = Product.objects.get(category__slug=self.kwargs['category'], slug=self.kwargs['product'])
        return obj


class ContactsView(TemplateView):
    template_name = 'contacts.html'
