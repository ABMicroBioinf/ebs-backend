from django.test import TestCase
from ..serializers import CompanySerializer
from sandbox.tests.factories import CompanyFactory
from ..models import Company

class CompanySerializerTestCase(TestCase):
    def test_model_fields(self):
       

        """Serializer data matches the Company object for each field."""
        company = CompanyFactory()
        serializer = CompanySerializer(company)
        
        for field_name in [
            'id', 'name', 'description', 'website', 'street_line_1', 'street_line_2',
            'city', 'state', 'zipcode'
        ]:
            
            self.assertEqual(
                serializer.data[field_name],
                getattr(company, field_name)
            )
       