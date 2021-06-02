from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone

from NEMO.models import UsageEvent, Tool, User


def metrics(request):
    tool_results = tool_usage(request)
    user_results = user_usage(request)

    return render(request, "NEMO_facility_metrics/metrics_dashboard.html",
                  {'tools': tool_results, 'users': user_results})


def tool_usage(request):
    tool_results = Tool.objects.all()
    start_period = timezone.now() + timedelta(days=-365)
    end_period = timezone.now()
    for tool in tool_results:
        # total_usage_period = sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(tool=tool, end__isnull=False, start__gt=start_period, end__lte=end_period)])
        total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                           UsageEvent.objects.filter(tool=tool, end__isnull=False)])
        tool.display_duration = display_duration(total_usage)
        percentage_duration = total_usage / (end_period - start_period).total_seconds()
        tool.display_percentage_duration = f"{percentage_duration:.0%}"

    return


def user_usage(request):
    results = User.objects.all()
    start_period = timezone.now() + timedelta(days=-365)
    end_period = timezone.now()
    for user in results:
        # total_usage_period = sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(tool=tool, end__isnull=False, start__gt=start_period, end__lte=end_period)])
        total_usage = sum([period(usage, period_start=start_period, period_end=end_period) for usage in
                           UsageEvent.objects.filter(user=user, end__isnull=False)])
        user.display_duration = display_duration(total_usage)
        percentage_duration = total_usage / (end_period - start_period).total_seconds()
        user.display_percentage_duration = f"{percentage_duration:.0%}"





def display_duration(seconds):
    duration = timedelta(seconds=seconds)
    return f'{duration.days * 24 + duration.seconds // 3600} hours, {duration.seconds % 3600 // 60} minutes '
    # return f'{duration.days} days, {duration.days * 24 + duration.seconds // 3600} hours, {duration.seconds % 3600 // 60} minutes '




    # def user_usage(request):
    # # usages = UsageEvent.objects.all()
    # results = {}
    # for user in User.objects.all():
    #     results[user.name] = sum(
    #         [usage.duration().total_seconds() for usage in UsageEvent.objects.filter(user=user, end__isnull=False)])
    #
    #  return render(request, "NEMO_facility_metrics/metrics_dashboard.html", {'usage': user, 'duration_result': results})results = {}



def period(usage: UsageEvent, period_start, period_end):
    usage_start = usage.start
    usage_end = usage.end

    # case 3
    if period_start <= usage_start <= period_end and period_end >= usage_end >= period_start:
        return usage.duration().total_seconds()
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
