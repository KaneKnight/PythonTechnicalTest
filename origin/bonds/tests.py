from django.test import TestCase
from .models import Bond

class BondTestCase(TestCase):
    def setUp(self):
        Bond.objects.create(isin="X10146", size=10, currency="GBP", maturity="2000-01-01", lei="1234", legal_name="Fake", userid=1)

    def test_bond_creation(self):
        """Animals that can speak are correctly identified"""
        fake = Bond.objects.get(isin="X10146")
        self.assertEqual(fake.lei, "1234")