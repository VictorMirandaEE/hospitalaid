from django.core import mail
from django.test import TestCase
from django.urls import reverse

from main import models


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_user_signup_page_submission_works(self):
        post_data = {
            "email": "user@domain.com",
        }
        response = self.client.post(reverse("signup"), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.User.objects.filter(email="user@domain.com").exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Hospital Aid Login Link")

    def test_step2_create_hospital_if_not_exists(self):
        user1 = models.User.objects.create_user("user1@domain.com", "pw432joij")
        post_data = dict(
            name="John smith",
            phone="123",
            hospital_name="Red cross",
            hospital_address="1 road street",
            hospital_city="London",
            hospital_postcode="XXX",
            hospital_country="United kingodm",
            hospital_latitude=12.1,
            hospital_longitude=22.3,
        )

        self.client.force_login(user1)
        response = self.client.post(reverse("signup_step2"), post_data)

        hospital = models.main.Hospital.objects.get(user=user1)
        self.assertEqual(hospital.name, "Red cross")

    def test_step2_change_hospital_if_exists(self):
        user1 = models.User.objects.create_user("user1@domain.com", "pw432joij")
        models.main.Hospital.objects.create(
            user=user1,
            name="White cross",
            address="2 black st",
            city="London",
            postal_code="?",
            country="KKK",
            latitude=1.1,
            longitude=2.2,
        )

        post_data = dict(
            name="John smith",
            phone="123",
            hospital_name="Red cross",
            hospital_address="1 road street",
            hospital_city="London",
            hospital_postcode="XXX",
            hospital_country="United kingodm",
            hospital_latitude=12.1,
            hospital_longitude=22.3,
        )

        self.client.force_login(user1)
        response = self.client.post(reverse("signup_step2"), post_data)

        hospital = models.main.Hospital.objects.get(user=user1)
        self.assertEqual(hospital.name, "Red cross")
