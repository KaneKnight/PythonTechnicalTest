from django.test import TestCase
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class BondTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

        self.bond1 = {
            "isin":"X10146",
            "size":10,
            "currency":"GBP",
            "maturity":"2000-01-01",
            "lei":"54321",
            "legal_name":"Fake1",
        }

        self.bond2 = {
            "isin":"Y10146",
            "size":10,
            "currency":"GBP",
            "maturity":"2000-01-01",
            "lei":"12345",
            "legal_name":"Fake2",
        }

        self.bond3 = {
            "isin":"Z10146",
            "size":10,
            "currency":"EUR",
            "maturity":"2000-01-01",
            "lei":"54321",
            "legal_name":"Fake1",
        }

        self.postbond = {
                "isin": "FR0000131104",
                "size": 100000000,
                "currency": "EUR",
                "maturity": "2025-02-28",
                "lei": "R0MUWSFPU8MPRO8K5P83"
        }

    def test_bond_creation(self):
        Bond.objects.create(isin="Hello", size=100, currency="GBP", maturity="2000-01-02", lei="1234", legal_name="Fake", userid=20)
        fake = Bond.objects.get(isin="Hello")
        self.assertEqual(fake.lei, "1234")

    def test_bond_post(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        res = client.post("/bonds/", self.postbond, format="json")
        created = Bond.objects.get(isin="FR0000131104")

        self.assertEqual(created.legal_name, "BNPPARIBAS")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_bond_get(self):
        Bond.objects.create(userid=self.user.id, **self.bond1)
        client = APIClient()
        client.force_authenticate(user=self.user)

        res = client.get("/bonds/")

        self.assertEqual(res.data, [self.bond1])

    def test_many_bond_get(self):
        Bond.objects.create(userid=self.user.id, **self.bond1)
        Bond.objects.create(userid=self.user.id, **self.bond2)
        client = APIClient()
        client.force_authenticate(user=self.user)

        res = client.get("/bonds/")

        self.assertEqual(res.data, [self.bond1, self.bond2])

    def test_bond_query(self):
        Bond.objects.create(userid=self.user.id, **self.bond1)
        Bond.objects.create(userid=self.user.id, **self.bond2)
        Bond.objects.create(userid=self.user.id, **self.bond3)
        client = APIClient()
        client.force_authenticate(user=self.user)

        res = client.get("/bonds/?legal_name=Fake1")

        self.assertEqual(res.data, [self.bond1, self.bond3])
