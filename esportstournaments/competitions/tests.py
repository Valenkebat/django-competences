from django.test import TestCase
from .models import Competition


class CompetitionTestCase(TestCase):
    def setUp(self):
        Competition.objects.create(name="torneo1",type="liga",phase=1,user="",teams=[1,2,3,4])
        Competition.objects.create(name="torneo2",type="elimination",phase=1,user="",teams=[1,2,3,4])


    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Competition.objects.get(name="torneo1")
        cat = Competition.objects.get(name="torneo2")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')