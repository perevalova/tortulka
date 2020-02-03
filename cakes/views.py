from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main.html'


class CategoryView(TemplateView):
    template_name = 'categories_list.html'


class CakeList(TemplateView):
    template_name = 'cakes_list.html'


class CakeDetail(TemplateView):
    template_name = 'cake_detail.html'


class ContactsView(TemplateView):
    template_name = 'contacts.html'
