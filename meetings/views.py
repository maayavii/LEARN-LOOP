from django.shortcuts import render
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AgoraView(View):
    app_id = 'ce4aa18557874e849332c58a21d828f0'

    def get(self, request, channel):
        try:
            if not channel or len(channel) > 64:  # Agora channel name limitations
                raise ValidationError("Invalid channel name")
            
            return render(request, 'agora_page.html', {
                'app_id': self.app_id,
                'channel': channel,
                'message': f"Agora connected on Channel '{channel}'"
            })
        except ValidationError as e:
            return render(request, 'agora_page.html', {
                'error': str(e)
            })
            
# meetings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Meeting
import uuid

class AgoraView(View):
    app_id = 'your_agora_app_id'

    def get(self, request, channel):
        meeting = get_object_or_404(Meeting, channel_name=channel)
        # Check if the current user is the host
        is_host = request.user == meeting.host
        return render(request, 'agora_page.html', {
            'app_id': self.app_id,
            'channel': channel,
            'is_host': is_host
        })


class CreateMeetingView(LoginRequiredMixin, View):
    def get(self, request):
        # Get user's meetings
        user_meetings = Meeting.objects.filter(host=request.user).order_by('-created_at')
        return render(request, 'create_meeting.html', {
            'user_meetings': user_meetings
        })
    
    def post(self, request):
        title = request.POST.get('title')
        scheduled_time = request.POST.get('scheduled_time')
        # Generate channel name using uuid4
        channel_name = str(uuid.uuid4())[:8]
        
        meeting = Meeting.objects.create(
            title=title,
            channel_name=channel_name,
            host=request.user,
            scheduled_time=scheduled_time,
            is_active=True
        )
        
        # Redirect to the Agora view with the channel
        return redirect('agora_view', channel=channel_name)

class MeetingListView(LoginRequiredMixin, View):
    def get(self, request):
        meetings = Meeting.objects.filter(host=request.user).order_by('-created_at')
        return render(request, 'meeting_list.html', {
            'meetings': meetings
        })
        
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import PermissionDenied

# meetings/views.py
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

# meetings/views.py
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

class EndMeetingView(LoginRequiredMixin, View):
    def post(self, request, channel_name):
        try:
            meeting = get_object_or_404(Meeting, channel_name=channel_name)
            
            if meeting.host != request.user:
                messages.error(request, "You are not authorized to end this meeting.")
                return redirect('meeting_list')

            # End the meeting in the database
            meeting.end_meeting()
            
            # Get channel layer and send message synchronously
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'meeting_{channel_name}',
                {
                    'type': 'meeting_ended'
                }
            )
            
            messages.success(request, "Meeting has been ended successfully.")
            return redirect('meeting_ended')
            
        except Exception as e:
            logger.error(f"Error ending meeting: {str(e)}")
            messages.error(request, "Error ending meeting. Please try again.")
            return redirect('meeting_list')

class MeetingEndedView(View):
    def get(self, request):
        return render(request, 'meeting_ended.html')