from datetime import datetime

from NEMO.models import User, Tool, Area, AreaAccessRecord, Account, Project, UsageEvent
from NEMO.tests.test_utilities import login_as_user, test_response_is_failed_login, login_as_staff
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
        owner = User.objects.create(username='mctest', first_name='Testy', last_name='McTester')
        tool = Tool.objects.create(name='test_tool', primary_owner=owner, _category='Imaging')
        area = Area.objects.create(name='Cleanroom', welcome_message='')
        account = Account.objects.create(name="account1")
        project = Project.objects.create(name="project1", account=account)

    def test_status_dashboard(self):
        login_as_user(self.client)
        response = self.client.get(reverse('status_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)

        # Test elif interest tools line 32
        response = self.client.get(reverse('status_dashboard'), data={'interest': 'tools'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # Test elif interest occupancy line 37
        response = self.client.get(reverse('status_dashboard'), data={'interest': 'occupancy'}, follow=True)
        self.assertEqual(response.status_code, 200)

        # create area records for testing line 56 status_dashboard.py
        login_as_staff(self.client)  # login_as_staff needed for line 45 in status_dashboard.py
        area_record = AreaAccessRecord()
        area_record.area = area
        area_record.customer = owner
        area_record.project = project
        area_record.start = datetime.now()
        area_record.save()

        response = self.client.get(reverse('status_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)

        #test usage_event line 191
        usage_event= UsageEvent()
        usage_event.user = owner
        usage_event.operator = owner
        usage_event.tool = tool
        usage_event.project = project
        usage_event.start = datetime.now()
        usage_event.save()

        response = self.client.get(reverse('status_dashboard'), follow=True)
        self.assertEqual(response.status_code, 200)

        #unavailable resource line 91, creat resource with available field = false line 1550 models.py

        #scheduled_outage line 94 outage started less than now and ends greater than now start__lte, end_gt Django queryset
        #create time in future in python
