from django.urls import path
from .views import AgoraView, CreateMeetingView, MeetingListView
from . import views
urlpatterns = [
    path('agora/<str:channel>/', AgoraView.as_view(
        app_id='ce4aa18557874e849332c58a21d828f0'
    ), name='agora_view'),
    path('create/', CreateMeetingView.as_view(), name='create_meeting'),
    path('list/', MeetingListView.as_view(), name='meeting_list'),
    path('meeting/<str:channel_name>/end/', views.EndMeetingView.as_view(), name='end_meeting'),
    path('end_meeting/<str:channel_name>/', views.EndMeetingView.as_view(), name='end_meeting'),
     # In urls.py

path('meeting_ended/', views.MeetingEndedView.as_view(), name='meeting_ended'),

]
