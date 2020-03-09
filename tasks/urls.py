from django.urls import re_path

from tasks.views import (
    Schedule,
    Details,
    ResetDetails, Reset)

app_name = 'tasks'
urlpatterns = [
    re_path(r'^schedule/$', Schedule.as_view(), name='schedule'),
    re_path(r'^reset/details/$', ResetDetails.as_view(), name='reset_details'),
    re_path(r'^reset/$', Reset.as_view(), name='reset'),
    re_path(r'^details/(?P<code>[\w-]+)/$', Details.as_view(), name='detauls'),
]
