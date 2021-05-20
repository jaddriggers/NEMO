from django.test import TestCase

from django.urls import reverse
from tests.test_utilities import login_as_user


class TestAlerts(TestCase):

    def test_alerts(self):
        login_as_user(self.client)

        #test GET
        response = self.client.get(reverse("alerts"), follow=True)
        self.assertEqual(response.status_code, 200)

        #test POST
            #pass data from AlertForm line 1819 models.py contents, creation_time, debut_time are required. use strftime() for debut_time. Has it been deleted?
        # response = self.client.get(reverse("alerts", data={}), follow=True)
        # self.assertEqual(response.status_code, 200)