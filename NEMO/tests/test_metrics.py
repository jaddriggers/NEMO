from datetime import datetime, timedelta

from django.utils import timezone

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
    Task,
)
from NEMO.tests.test_utilities import (
    login_as_user,
    test_response_is_failed_login,
    login_as_staff,
)
from NEMO.views.customization import set_customization, get_customization
from django.test import TestCase
from django.urls import reverse


class MetricTestCase(TestCase):
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


    def test_metrics(self):
        login_as_user(self.client)

        # test tool_usage()
        usage_event = UsageEvent()
        usage_event.user = owner
        usage_event.tool = tool
        usage_event.start = timezone.now() + timedelta(days=-30)
        usage_event.end = timezone.now()
        #usage_event.save()

        response = self.client.get(reverse("facility_metrics"), follow=True)
        self.assertEqual(response.status_code, 200)