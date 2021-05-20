from django.test import TestCase
from django.urls import reverse
from NEMO.models import ReservationItemType

from tests.test_utilities import login_as_user


class SidebarTestCase(TestCase):



    def test_refresh_sidebar(self):

        login_as_user(self.client)

        #test area elif
        response = self.client.get(
            reverse("refresh_sidebar_icons", kwargs={"item_type": ReservationItemType.AREA.value}), follow=True
        )
        self.assertEqual(response.status_code, 200)

        #test tool elif
        response = self.client.get(
            reverse("refresh_sidebar_icons", kwargs={"item_type": ReservationItemType.TOOL.value}), follow=True
        )
        self.assertEqual(response.status_code, 200)