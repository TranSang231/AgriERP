from os.path import join
from django.conf import settings
from oauth.models.user import User
from ..models import UserToken, NotificationImage
from base.services.base import BaseService

import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, messaging
from django.shortcuts import get_object_or_404
from django.core.files import File

# Initialize the Firebase Admin SDK
credential_file = join(settings.BASE_DIR, "firebase",
                       "credentials", "serviceAccountKey.json")
cred = credentials.Certificate(credential_file)
firebase_admin.initialize_app(cred)


class CloudMessageService(BaseService):

    @classmethod
    def upload_image(cls, local_file_path):
        """
        Upload a local image to Django media storage and return the public URL

        Args:
            local_file_path: Path to the local image file

        Returns:
            str: Public URL of the uploaded image
        """
        try:
            # Generate a unique filename
            filename = os.path.basename(local_file_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"

            # Create NotificationImage instance
            with open(local_file_path, 'rb') as f:
                notification_image = NotificationImage()
                notification_image.image.save(
                    unique_filename, File(f), save=True)

            # Get the public URL
            image_url = notification_image.get_image_url()
            print(f"Image uploaded successfully. URL: {image_url}")

            return image_url

        except Exception as e:
            print(f"Error uploading image: {str(e)}")
            return None

    @classmethod
    def send_cloud_message(cls, user_id, title='', body='', local_image_path=None):
        """
        Send FCM notification with optional image to a user's devices

        Args:
            user_id: The ID of the user to send notification to
            title: Notification title (string)
            body: Notification body (string)
            local_image_path: Optional image to include in notification
        """
        # First upload the image if provided
        image_url = None
        if local_image_path and os.path.exists(local_image_path):
            image_url = cls.upload_image(local_image_path)
            if not image_url:
                print("Failed to upload image, sending notification without image")

        user = get_object_or_404(User, id=user_id)

        # Get all tokens for the user
        user_tokens = [
            user_token.token for user_token in UserToken.objects.filter(user_id=user.id)
        ]
        print(f"user_tokens: {user_tokens}")

        # Create APNS config with image
        apns = messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    mutable_content=True,
                    content_available=True,
                    custom_data={
                        'priority': 'high',
                    }
                )
            ),
            fcm_options=messaging.APNSFCMOptions(
                image=image_url
            ) if image_url else None
        )

        # Create Android notification config with image
        android = messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                image=image_url
            )
        ) if image_url else None

        # Create the message payload
        message = messaging.MulticastMessage(
            tokens=user_tokens,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            apns=apns,
            android=android
        )

        # Send the message
        response = messaging.send_each_for_multicast(multicast_message=message)
        success_message = f'{
            response.success_count} messages were sent successfully'
        print(success_message)

        return success_message
