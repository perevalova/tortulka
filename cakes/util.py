import time

from django.contrib.sites.models import Site
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.template.loader import render_to_string
from django.urls import reverse

from tortulka.settings import SEPARATOR
from .encryption_util import encrypt
from .models import Subscriber
from .tasks import send_news_email


def paginate(objects, size, request, context, var_name='object_list'):
    """Paginate objects provided by view.

    This function takes:
    * list of elements;
    * number of objects per page;
    * request object to get url parameters from;
    * context to set new variables into;
    * var_name - variable name for list of objects.

    It returns updated context object.
    """

    # apply pagination
    paginator = Paginator(objects, size)

    # try to get page number from request
    page = request.GET.get('page', 1)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        object_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999),
        # deliver last page of results
        object_list = paginator.page(paginator.num_pages)

    # set variables into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context


def filtering(request, object_list):
    """Filter objects provided by view.

    This function takes:
    * request:
    * list of elements;

    It returns filtered Queryset.
    """

    # searching
    search_product = request.GET.get('q', '')
    if search_product:
        object_list = object_list.filter(
            title__icontains=search_product)

    # filter by category
    category_filter = request.GET.get('category', '')
    if category_filter == 'all':
        object_list = object_list
    elif category_filter:
        object_list = object_list.filter(category__slug=category_filter)

    # filter by tiers
    tiers_filter = request.GET.get('tiers', '')
    if tiers_filter == 'all':
        object_list = object_list
    elif tiers_filter:
        object_list = object_list.filter(category__slug=tiers_filter)

    # ordering
    order_by = request.GET.get('order_by', '')
    if order_by == 'newest':
        object_list = object_list.order_by('-added', 'id')
    elif order_by == 'oldest':
        object_list = object_list.order_by('added', 'id')
    elif order_by == 'abc':
        object_list = object_list.order_by('title', 'id')

    return object_list


def send_newsletter(subject, message):
    """
    Send letter to newsletter subscribers
    :param subject: str - subject of letter
    :param message:  str - message of letter
    :return: None
    """
    subscribers = list(Subscriber.objects.values_list('email', flat=True))
    for subscriber in subscribers:
        token = encrypt(subscriber + SEPARATOR + str(time.time()))
        url = reverse('unsubscribe')
        domain = Site.objects.get_current().domain
        confirmation_url = domain + url + '?token=' + token
        message = render_to_string('news_letter.html', {
            'message': message,
            'confirmation_url': confirmation_url
        })
        send_news_email.delay(subject, message, subscriber)


def send_subscription_email(email, url):
    """
    Send email to subscriber for confirmation subscription

    :param email: Subscriber email
    :param url: url to subscription confirmation page
    :return: None
    """
    token = encrypt(email + SEPARATOR + str(time.time()))
    confirmation_url = url + '?token=' + token
    mail_subject = 'Підтвердження підписки на розсилку'
    message = render_to_string('subscription.html', {
        'confirmation_url': confirmation_url
    })
    to_email = email
    send_news_email.delay(mail_subject, message, to_email)
