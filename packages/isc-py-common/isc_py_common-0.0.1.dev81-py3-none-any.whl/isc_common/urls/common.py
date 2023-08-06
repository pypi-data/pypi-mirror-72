from django.urls import path

from isc_common.views.common import Common_RemoveFile

urlpatterns = [

    path('Common/RemoveFile', Common_RemoveFile),

]
