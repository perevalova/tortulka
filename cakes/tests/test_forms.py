from django.core import mail
from django.test import TestCase
from django.urls import reverse

from cakes.forms import ContactForm


class ContactFormTest(TestCase):

    def test_fields(self):
        data_form = {
            'first_name': 'Anna',
            'last_name': 'Smith',
            'email': 'testemail@email.com',
            'phone_number': '+380986458956',
            'message': 'Hello'
        }
        form = ContactForm(data=data_form)
        self.assertTrue(form.is_valid())

    def test_blank_phone_number(self):
        data_form = {
            'first_name': 'Anna',
            'last_name': 'Smith',
            'email': 'testemail@email.com',
            'phone_number': '',
            'message': 'Hello'
        }
        form = ContactForm(data=data_form)
        # test that phone number can be missed
        self.assertTrue(form.is_valid())

    def test_phone_number(self):
        data_form = {
            'first_name': 'Anna',
            'last_name': 'Smith',
            'email': 'testemail@email.com',
            'phone_number': '380674568958',
            'message': 'Hello'
        }
        field = 'phone_number'
        response = self.client.post(reverse('contacts'), data_form)
        errors = ['Формат номеру: +380123456789', 'Переконайтеся, що це значення містить не менш ніж 13 символів (зараз 12).']
        # test phone number validation
        self.assertFormError(response, 'form', field, errors)

    def test_send_email(self):
        data_form = {
            'first_name': 'Anna',
            'last_name': 'Smith',
            'email': 'testemail@email.com',
            'phone_number': '+380674568958',
            'message': 'Hello'
        }
        response = self.client.post(reverse('contacts'), data_form)
        subject = 'Anna Smith, testemail@email.com, +380674568958'

        # test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].from_email, 'testemail@email.com')
        self.assertEqual(mail.outbox[0].body, 'Hello')
