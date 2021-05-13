from io import StringIO
from django.urls import reverse
from NEMO.models import User, Tool, Area
from NEMO.tests.test_utilities import (
    login_as_user,
    test_response_is_failed_login,
    login_as_staff,
)
from NEMO.views.customization import (
    set_customization,
    get_customization,
    store_media_file,
)
from django.test import TestCase
from utilities import send_mail, EmailCategory
from django.template import Template, RequestContext, Context


class TestFacilityRules(TestCase):

    # Test GET
    def test_facility_rules(self):
        login_as_user(self.client)
        content = StringIO("Jad")
        store_media_file(content, "facility_rules_tutorial.html")
        response = self.client.get(reverse("facility_rules"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jad", None, 200)

    # Test POST line 23
    def test_facility_rules_Post(self):
        login_as_user(self.client)
        content = StringIO("Jad")
        set_customization("abuse_email_address", "test@test.com")
        store_media_file(content, "facility_rules_tutorial_email.html")
        response = self.client.post(reverse("facility_rules"), follow=True)
        self.assertEqual(response.status_code, 200)
