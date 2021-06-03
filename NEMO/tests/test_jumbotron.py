from tests.test_utilities import login_as_user
from django.test import TestCase
from django.urls import reverse

class JumbotronTestCase(TestCase):

    def test_jumbotron(self):
        login_as_user(self.client)
        response = self.client.get(reverse("jumbotron"), follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('jumbotron_content'), follow=True)
        self.assertEqual(response.status_code, 200)