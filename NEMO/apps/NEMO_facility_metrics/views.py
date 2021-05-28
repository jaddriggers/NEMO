from datetime import datetime, timedelta

from django.shortcuts import render
from NEMO.models import UsageEvent, Tool, User
from NEMO.views.pagination import SortedPaginator
from django.db.models import Avg, Count, Min, Sum

#Option 1 Iterating over a dictionary
# def tool_usage(request):
#     usages = UsageEvent.objects.all()
#     result = {}
#     for usage in usages:
#         if usage.tool.name in result:
#             result[usage.tool.name] = result[usage.tool.name] + usage.duration()
#         else:
#             result[usage.tool.name] = usage.duration()
#     return render(request, "NEMO_facility_metrics/metrics_dashboard.html",
#                   {'usages': usages, 'duration_result': result})

#Option 2 using sum

# def tool_usage(request):
#     # usages = UsageEvent.objects.all()
#     results = {}
#     for tool in Tool.objects.all():
#         results[tool.name] = display_duration(sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(tool=tool, end__isnull=False)]))
#
#     return render(request, "NEMO_facility_metrics/metrics_dashboard.html", {'usage': tool , 'duration_result': results})

def tool_usage(request):
    # usages = UsageEvent.objects.all()
    results = Tool.objects.all()

    start_period = datetime.now() + timedelta(days= -1)
    end_period = datetime.now()
    for tool in results:
        total_usage_period = sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(tool=tool, end__isnull=False, start__gt=start_period, end__lte=end_period)])
        total_usage = sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(tool=tool, end__isnull=False)])
        tool.display_duration = display_duration(total_usage)
        percentage_duration = total_usage_period / (end_period - start_period).total_seconds()
        tool.display_percentage_duration = f"{percentage_duration:.0%}"

    return render(request, "NEMO_facility_metrics/metrics_dashboard.html", {'tools': results})

def display_duration(seconds):

    duration = timedelta(seconds=seconds)
    return f'{duration.days} days, {duration.seconds} seconds '


# get usage event time(end-start, duration in minutes-use duration function), djanogo annotate sum on field and put in total field

# def user_usage(request):
#     usages = UsageEvent.objects.all()
#     result = {}
#     for usage in usages:
#         if usage.user.username in result :
#             result[usage.user.username] = result[usage.user.username] + usage.duration()
#
#         else:
#             result[usage.user.username] = usage.duration()
#
#     return render(request, "NEMO_facility_metrics/metrics_dashboard.html",
#                   {'usages': usages, 'user_duration': result})


def user_usage(request):
    # usages = UsageEvent.objects.all()
    results = {}
    for user in User.objects.all():
        results[user.name] = sum([usage.duration().total_seconds() for usage in UsageEvent.objects.filter(user=user, end__isnull=False)])

    return render(request, "NEMO_facility_metrics/metrics_dashboard.html", {'usage': user , 'duration_result': results})

