from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@receiver(m2m_changed, sender=Notification.recievers.through)
def send_notification_to_users(sender, instance, action, **kwargs):
    if action == "post_add":
        print("Signal Triggered: post_add")
        channel_layer = get_channel_layer()
        for receiver in instance.recievers.all():
            notification_message = {
                'notification': instance.message,
                'sender': instance.sender.username,
                'type': instance.type,
            }
            try:
                async_to_sync(channel_layer.group_send)(
                    f"user_notifications_{receiver.id}",
                    {
                        'type': 'send_notification',
                        'notification': notification_message
                    }
                )
                print(f"Notification sent to user_notifications_{receiver.id}")
            except Exception as e:
                print("failed", e)
