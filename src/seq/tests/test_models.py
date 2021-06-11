from django.test import TestCase

from ..models import Study
from seq.tests.factories import StudyFactory


class StudyTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        study = StudyFactory()
        
        self.assertEqual(str(study), study.title)