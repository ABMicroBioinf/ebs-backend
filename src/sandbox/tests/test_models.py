from django.test import TestCase

from ..models import Company
from sandbox.tests.factories import CompanyFactory


class CompanyTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        company = CompanyFactory()
        
        self.assertEqual(str(company), company.name)