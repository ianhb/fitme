# Create your tests here.
from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail("Subject", "Message", 'ianhblakley@gmail.com', ['ihb9@cornell.edu'], fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
