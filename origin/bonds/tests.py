from django.test import TestCase
from .models import Bond
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status


class BondTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = User.objects.create_user(username='test', password='test')

    def test_bond_creation(self):
        Bond.objects.create(isin="X10146", size=10, currency="GBP", maturity="2000-01-01", lei="1234", legal_name="Fake", userid=1)
        fake = Bond.objects.get(isin="X10146")
        self.assertEqual(fake.lei, "1234")

    def test_bond_post(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        bond = {
            "isin": "FR0000131104",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83"
        }
        res = client.post("/bonds/", bond, format="json")
        
        created = Bond.objects.get(isin="FR0000131104")
        self.assertEqual(created.legal_name, "BNPPARIBAS")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_bond_get(self):
        bond = {
            "isin":"X10146",
            "size":10,
            "currency":"GBP",
            "maturity":"2000-01-01",
            "lei":"1234",
            "legal_name":"Fake",
        }
        Bond.objects.create(userid=self.user.id, **bond)
        client = APIClient()
        client.force_authenticate(user=self.user)

        res = client.get("/bonds/")

        self.assertEqual(res.data, [bond])