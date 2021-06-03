from datetime import datetime, timedelta
from typing import Tuple

from django.shortcuts import render
from django.utils import timezone

from NEMO.models import UsageEvent, Tool, User, Project, ScheduledOutage, Resource


# gets period from date filter request
def get_period_from_request(request) -> Tuple[datetime, datetime]:
    period = request.GET.get("period")
    right_now = timezone.now()

    if period == 'last_60_days':
        return right_now + timedelta(days=-60), right_now

    elif period == 'last_90_days':
        return right_now + timedelta(days=-90), right_now

    else:
        return right_now + timedelta(days=-30), right_now

    # elif period == 'this_year':
    #     return right_now + timedelta(days=-90), right_now datetime.now replace month = 1, day = 1, give the first of each year






def metrics(request):
    start, end = get_period_from_request(request)
    tool_results = tool_usage(start, end)
    period = get_period_from_request(request)
    # user_results = user_usage(request)
    # project_results = project_usage(request)
    # outage_results = scheduled_outage(request)

    return render(request, "NEMO_facility_metrics/metrics_dashboard.html", {'tools': tool_results, 'period': period})


# tool usage and outage duration
def tool_usage(start_period, end_period):
    tool_results = Tool.objects.all()
    for tool in tool_results:
        add_tool_usage(start_period, end_period, tool)
        add_tool_outage(start_period, end_period, tool)
        add_tool_full_resource_outage(start_period, end_period, tool)
        add_tool_partial_resource_outage(start_period, end_period, tool)

    return tool_results


def add_tool_usage(start_period, end_period, tool):
    total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                       UsageEvent.objects.filter(tool=tool, end__isnull=False)])
    tool.display_duration = display_duration(total_usage)
    percentage_duration = total_usage / (end_period - start_period).total_seconds()
    tool.display_percentage_duration = f"{percentage_duration:.0%}"


def add_tool_outage(start_period, end_period, tool):
    total_outage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                        ScheduledOutage.objects.filter(tool=tool, end__isnull=False)])
    tool.display_outage_duration = display_duration(total_outage)
    percentage_outage_duration = total_outage / (end_period - start_period).total_seconds()
    tool.display_outage_percentage_duration = f"{percentage_outage_duration:.0%}"


def add_tool_full_resource_outage(start_period, end_period, tool):
    total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                       ScheduledOutage.objects.filter(resource__fully_dependent_tools__in=[tool],
                                                      end__isnull=False)])
    tool.resource_display_duration = display_duration(total_usage)
    percentage_resource_duration = total_usage / (end_period - start_period).total_seconds()
    tool.display_resource_percentage_duration = f"{percentage_resource_duration:.0%}"


def add_tool_partial_resource_outage(start_period, end_period, tool):
    total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                       ScheduledOutage.objects.filter(resource__partially_dependent_tools__in=[tool],
                                                      end__isnull=False)])
    tool.resource_display_duration = display_duration(total_usage)
    percentage_resource_partial_duration = total_usage / (end_period - start_period).total_seconds()
    tool.display_resource_percentage_partial_duration = f"{percentage_resource_partial_duration:.0%}"


# scheduled outage duration
def scheduled_outage(request):
    tool_outage_results = Tool.objects.all()
    start_period = timezone.now() + timedelta(days=-30)
    end_period = timezone.now()
    for tool in tool_outage_results:
        total_outage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                            ScheduledOutage.objects.filter(tool=tool, end__isnull=False)])
        tool.display_duration = display_duration(total_outage)
        percentage_duration = total_outage / (end_period - start_period).total_seconds()
        tool.display_percentage_duration = f"{percentage_duration:.0%}"

    return tool_outage_results


# user usage duration
def user_usage(request):
    user_results = User.objects.all()
    start_period = timezone.now() + timedelta(days=-30)
    end_period = timezone.now()
    for user in user_results:
        total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                           UsageEvent.objects.filter(user=user, end__isnull=False)])
        user.display_duration = display_duration(total_usage)
        percentage_duration = total_usage / (end_period - start_period).total_seconds()
        user.display_percentage_duration = f"{percentage_duration:.0%}"

    return user_results


# project usage duration
def project_usage(request):
    project_results = Project.objects.all()
    start_period = timezone.now() + timedelta(days=-30)
    end_period = timezone.now()
    for project in project_results:
        total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                           UsageEvent.objects.filter(project=project, end__isnull=False)])
        project.display_duration = display_duration(total_usage)
        percentage_duration = total_usage / (end_period - start_period).total_seconds()
        project.display_percentage_duration = f"{percentage_duration:.0%}"

    return project_results


# does conversion to show usage in days, hours and minutes
def display_duration(seconds):
    duration = timedelta(seconds=seconds)

    return f'{duration.days} days, {duration.seconds // 3600} hours, {duration.seconds % 3600 // 60} minutes '
    # return f'{duration.days} days, {duration.days * 24 + duration.seconds // 3600} hours, {duration.seconds % 3600 // 60} minutes '


# usage period requested by user
def period(usage: UsageEvent, period_start, period_end):
    usage_start = usage.start
    usage_end = usage.end

    # case 3
    if period_start <= usage_start <= period_end and period_end >= usage_end >= period_start:
        return (usage.end - usage.start).total_seconds() if usage.end and usage.start else 0
    # case 1,5
    elif (usage_start < period_start and usage_end < period_start) or (usage_start > period_end):
        return 0
    # case 6
    elif usage_start < period_start and usage_end > period_end:
        return (period_end - period_start).total_seconds()
    # case 2
    elif usage_start < period_start and usage_end > period_start and usage_end < period_end:
        return (usage_end - period_start).total_seconds()
    # case 4
    elif usage_start < period_end and usage_start > period_start and usage_end > period_end:
        return (period_end - usage_start).total_seconds()
