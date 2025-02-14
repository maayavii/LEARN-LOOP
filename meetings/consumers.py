# meetings/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)

class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_name = self.scope['url_route']['kwargs']['channel_name']
        self.meeting_group_name = f'meeting_{self.channel_name}'
        
        logger.info(f"WebSocket connecting to meeting: {self.channel_name}")
        
        # Join meeting group
        await self.channel_layer.group_add(
            self.meeting_group_name,
            self.channel_name
        )
        
        logger.info(f"Added to group: {self.meeting_group_name}")
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnecting from meeting: {self.channel_name}")
        await self.channel_layer.group_discard(
            self.meeting_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            logger.info(f"Received WebSocket message: {text_data}")
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            logger.info(f"Processing message type: {message_type}")
            
            if message_type == 'end_meeting':
                logger.info(f"Broadcasting end_meeting to group: {self.meeting_group_name}")
                await self.channel_layer.group_send(
                    self.meeting_group_name,
                    {
                        'type': 'meeting_ended'
                    }
                )
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    async def meeting_ended(self, event):
        try:
            logger.info("Sending meeting_ended event to client")
            await self.send(text_data=json.dumps({
                'type': 'meeting_ended'
            }))
            logger.info("Successfully sent meeting_ended event")
        except Exception as e:
            logger.error(f"Error sending meeting_ended event: {str(e)}")