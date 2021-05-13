from datetime import datetime, timedelta

from NEMO.models import (
    User,
    Tool,
    Area,
    AreaAccessRecord,
    Account,
    Project,
    UsageEvent,
    Resource,
    ResourceCategory,
    ScheduledOutage,
)
from NEMO.tests.test_utilities import (
    login_as_user,
    test_response_is_failed_login,
    login_as_staff,
)
from NEMO.views.customization import set_customization, get_customization
from django.test import TestCase
from django.urls import reverse


class StatusDashboardTestCase(TestCase):
    tool: Tool = None
    owner: User = None
    area: Area = None
    account: Account = None
    project: Project = None

    def setUp(self):
        global tool, owner, area, project
        owner = User.objects.create(
            username="mctest", first_name="Testy", last_name="McTester"
        )
        tool = Tool.objects.create(
            name="test_tool", primary_owner=owner, _category="Imaging"
        )
        area = Area.objects.create(name="Cleanroom", welcome_message="")
        account = Account.objects.create(name="account1")
        project = Project.objects.create(name="project1", account=account)

    def test_status_dashboard(self):
        login_as_user(self.client)
        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # Test elif interest tools line 32
        response = self.client.get(
            reverse("status_dashboard"), data={"interest": "tools"}, follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Test elif interest occupancy line 37
        response = self.client.get(
            reverse("status_dashboard"), data={"interest": "occupancy"}, follow=True
        )
        self.assertEqual(response.status_code, 200)

        # create area records for testing line 56 status_dashboard.py
        login_as_staff(
            self.client
        )  # login_as_staff needed for line 45 in status_dashboard.py
        area_record = AreaAccessRecord()
        area_record.area = area
        area_record.customer = owner
        area_record.project = project
        area_record.start = datetime.now()
        area_record.save()

        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # test usage_event
        usage_event = UsageEvent()
        usage_event.user = owner
        usage_event.operator = owner
        usage_event.tool = tool
        usage_event.project = project
        usage_event.start = datetime.now()
        usage_event.save()

        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # Test resource
        resource = Resource()
        resource_category = ResourceCategory()
        resource_category.save()
        resource.name = "Jad Test"
        resource.category = resource_category
        resource.available = False
        resource.save()
        resource.fully_dependent_tools.add(tool)
        resource.partially_dependent_tools.add(tool)
        resource.save()

        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # test scheduled_outage
        scheduled_outage = ScheduledOutage()
        scheduled_outage.tool = tool
        scheduled_outage.creator = owner
        scheduled_outage.start = datetime.now() - timedelta(days=1)
        scheduled_outage.end = datetime.now() + timedelta(days=1)
        scheduled_outage.save()

        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        #Test scheduled outage resource
        scheduled_outage = ScheduledOutage()
        scheduled_outage.creator = owner
        scheduled_outage.start = datetime.now() - timedelta(days=1)
        scheduled_outage.end = datetime.now() + timedelta(days=1)
        scheduled_outage.resource = resource
        scheduled_outage.save()

        response = self.client.get(reverse("status_dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)

        # test create_area_summary add_outages and add_resources

        scheduled_outage = ScheduledOutage()
        scheduled_outage.creator = owner
        scheduled_outage.start = datetime.now() - timedelta(days=1)
        scheduled_outage.end = datetime.now() + timedelta(days=1)
        scheduled_outage.resource = resource
        scheduled_outage.resource.dependent_areas.add(area)
        scheduled_outage.area = area

        scheduled_outage.save()

        response = self.client.get(reverse('refresh_sidebar_icons'), follow=True)
        self.assertEqual(response.status_code, 200)

        #Test add_occupants customer_display

