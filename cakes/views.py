import logging
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView

from smtplib import SMTPServerDisconnected, SMTPConnectError

from cakes.models import Category, Product, Subscriber
from tortulka.settings import  SEPARATOR
from .encryption_util import decrypt
from .forms import ContactForm, SubscriberForm
from .tasks import send_admin_email
from .util import paginate, filtering, send_subscription_email


class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()[:8].prefetch_related('category', 'images')
        context['form'] = SubscriberForm
        return context

    def post(self, request, *args, **kwargs):
        form = SubscriberForm(data=request.POST)
        if form.is_valid():
            url = request.build_absolute_uri(
                reverse('subscription_confirmation'))
            send_subscription_email(form.cleaned_data['email'], url)
            messages.success(self.request,
                             'Перевірте Вашу поштову скриньку та підтвердіть, будь ласка, підписку!')
        else:
            messages.warning(self.request, 'Ви вже підписані на розсилку!')
        return redirect('home')


class CategoryView(ListView):
    template_name = 'category_list.html'
    model = Category


class ProductList(ListView):
    """
    Page with product list for specific category
    """
    template_name = 'product_list.html'
    paginate_by = 12

    def get_queryset(self):
        product_list = Product.objects.filter(category__slug=self.kwargs['slug']).prefetch_related('category', 'images')

        # filter objects
        product_list = filtering(self.request, product_list)

        return product_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context = paginate(self.get_queryset(), self.paginate_by, self.request,
                           context)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])

        return context


class ProductDetail(DetailView):
    """
    Single product
    """
    model = Product
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        obj = Product.objects.prefetch_related(
                'category', 'images').get(category__slug=self.kwargs['category'], slug=self.kwargs['product'])
        return obj


class ContactsView(FormView):
    """
    Contact page with form for send email
    """
    template_name = 'contacts.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacts')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        phone_number = form.cleaned_data['phone_number']
        email = form.cleaned_data['email']
        subject = f'{first_name} {last_name}, {email}, {phone_number}'
        message = form.cleaned_data['message']

        # sending letter
        try:
            send_admin_email(subject, message, email)
            messages.success(self.request, 'Лист успішно надісланий!')
        except (SMTPServerDisconnected, SMTPConnectError):
            messages.warning(self.request,
                             'Під час надсилання листа сталася несподівана помилка. Спробуйте скористатися цією формою пізніше.')
            logger = logging.getLogger(__name__)
            logger.exception(messages)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Перевірте, будь ласка, форму на помилки.')
        logger = logging.getLogger(__name__)
        logger.exception(messages)
        return super().form_invalid(form)


class SearchView(ListView):
    """
    Searching for specific product
    """
    template_name = 'search.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        search_product = self.request.GET.get('q', '')
        products = Product.objects.none()
        if search_product:
            products = Product.objects.filter(title__search=search_product).prefetch_related('category', 'images')

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        product_amount = self.get_queryset().count()
        context = paginate(self.get_queryset(), self.paginate_by, self.request,
                           context, var_name='products')
        context['product_amount'] = product_amount

        return context


class RulesView(TemplateView):
    template_name = 'rules.html'


class AboutView(TemplateView):
    template_name = 'about.html'


def subscription_confirmation(request):
    if 'POST' == request.method:
        raise Http404

    token = request.GET.get('token', None)

    if not token:
        logging.getLogger('warning').warning('Invalid Link')
        messages.warning(request, 'Недійсне посилання')
        return redirect('home')

    token = decrypt(token)
    if token:
        token = token.split(SEPARATOR)
        email = token[0]
        try:
            subscribe_model_instance = Subscriber.objects.create(email=email)
            subscribe_model_instance.save()
            messages.success(request, 'Підписка успішно підтверджена! Дякую.')
        except Exception:
            logging.getLogger('warning').warning('Invalid Link')
            messages.warning(request, 'Недійсне посилання')
    else:
        logging.getLogger('warning').warning('Invalid token')
        messages.warning(request, 'Недійсне посилання')

    return redirect('home')


def unsubscribe(request):
    if 'POST' == request.method:
        raise Http404

    token = request.GET.get('token', None)

    if not token:
        logging.getLogger('warning').warning('Invalid Link')
        messages.warning(request, 'Недійсне посилання')
        return redirect('home')

    token = decrypt(token)
    if token:
        token = token.split(SEPARATOR)
        email = token[0]
        try:
            Subscriber.objects.get(email=email).delete()
            messages.success(request, 'Ви успішно відписалися від розсилки.')
        except Exception:
            logging.getLogger('warning').warning('Invalid Link')
            messages.warning(request, 'Недійсне посилання')
    else:
        logging.getLogger('warning').warning('Invalid token')
        messages.warning(request, 'Недійсне посилання')

    return redirect('home')