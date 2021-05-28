from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from NEMO.models import Alert
from NEMO.tests.test_utilities import login_as_staff, login_as_user
from NEMO.views import alerts


class TestAlerts(TestCase):

    def test_alerts(self):
        login_as_staff(self.client)

        #test GET
        response = self.client.get(reverse("alerts"), follow=True)
        self.assertEqual(response.status_code, 200)

        #test POST


        #318/319 from test_area_reservations to test it was created in database
        response = self.client.post(reverse("alerts"), data={'contents':'Test1','creation_time':'2018-06-21T21:02:26.460Z','debut_time': datetime.now().strftime('%m/%d/%Y %I:%M %p') }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.all().count(), 1)
        self.assertTrue(Alert.objects.get(contents='Test1'))

    def test_delete_alerts(self):
        login_as_staff(self.client)
        alert = Alert.objects.create(contents='Test', creation_time='2018-06-21T21:02:26.460Z', debut_time=datetime.now())
        self.assertEqual(Alert.objects.all().count(), 1)
        response = self.client.post(reverse('delete_alert', kwargs={"alert_id": alert.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.all().count(), 1)

    def test_delete_alerts2(self):
        user = login_as_user(self.client)
        alert = Alert.objects.create(contents='Test', user=user, creation_time='2018-06-21T21:02:26.460Z',debut_time=datetime.now())
        self.assertEqual(Alert.objects.all().count(), 1)
        response = self.client.post(reverse('delete_alert', kwargs={"alert_id": alert.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.all().count(), 1)

    # def test_except(self):
    #     response = self.client.get(reverse('delete_alert',kwargs={}), follow=True)
    #     self.assertRaises(response.status_code, 404)


