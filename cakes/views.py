from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView

from cakes.models import Category, Product
from tortulka.settings import CONTACT_EMAIL
from .forms import ContactForm
from .util import paginate

class MainPageView(TemplateView):
    template_name = 'main.html'


class CategoryView(ListView):
    template_name = 'category_list.html'
    model = Category


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    paginate_by = 12

    def get_queryset(self):
        product_list = Product.objects.filter(category__slug=self.kwargs['slug']).prefetch_related('category', 'images')

        order_by = self.request.GET.get('order_by', '')
        if order_by == 'newest':
            product_list = product_list.order_by('-added', 'id')
        elif order_by == 'oldest':
            product_list = product_list.order_by('added', 'id')
        elif order_by == 'abc':
            product_list = product_list.order_by('title', 'id')

        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        product_amount = self.get_queryset().count()
        context = paginate(self.get_queryset(), self.paginate_by, self.request,
                           context, var_name='products')
        context['product_amount'] = product_amount

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        obj = Product.objects.prefetch_related(
                'category', 'images').get(category__slug=self.kwargs['category'], slug=self.kwargs['product'])
        return obj


class ContactsView(FormView):
    template_name = 'contacts.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacts')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        subject = f'{first_name} {last_name}, {phone_number}'
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        send_mail(subject, message, email, [CONTACT_EMAIL])
        messages.success(self.request, 'Лист успішно надісланий!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Під час надсилання листа сталася несподівана помилка. Спробуйте скористатися цією формою пізніше.')
        return super().form_invalid(form)


class SearchView(ListView):
    template_name = 'search.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        search_product = self.request.GET.get('q', '')
        products = Product.objects.none()
        if search_product:
            products = Product.objects.filter(title__icontains=search_product).prefetch_related('category', 'images')

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        product_amount = self.get_queryset().count()
        context = paginate(self.get_queryset(), self.paginate_by, self.request,
                           context, var_name='products')
        context['product_amount'] = product_amount

        return context
